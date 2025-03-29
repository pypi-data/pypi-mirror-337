#!/bin/bash
#
# Creates a new release branch from origin/master, generates the v1.X.0
# release tag.
#
# If this script fails, you will need to generate the release manually. The
# instructions for manual release are here:
#
#    git checkout master
#    git pull
#    git checkout -b vX.y (X is major version, y is minor version. Should be aligned with github milestone)
#    git push --set-upstream origin vX.y
#    git tag vX.y.0
#    git push origin vX.y.0
#    gh release create vX.y.0 --verify-tag --generate-notes --title vX.Y.0 --notes-start-tag vX.{Y-1}.0
#
#    Alternatively, perform the last step in the UI: https://github.com/kumo-ai/kumo/releases/new

set -e

VERSION=$2
CI="${1:-false}"

if [[ $# -ne 1 && $# -ne 2 && $# -ne 3 ]]
then
  echo
  echo "Usage: ./scripts/release/start_release.sh <CI> <VERSION> <BASE_REF>"
  echo
  echo "  CI : Indicates if the script is run in CI"
  echo "  VERSION: The major version of the release, such as 'v1.9'"
  echo "  BASE_REF (optional): The git branch or commit that should "
  echo "    be used to create the release branch. Default: origin/master"
  echo
  exit 1
fi

if [[ ! "$VERSION" =~ ^v[0-9]\.[0-9]+$ ]];
then
  echo "Official release branches should have format such as v1.9 but got $VERSION"
  echo
  read -p "Do you wish to continue anyway? [Y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]
  then
    false
  fi
  NOTES_ARG=""
else
  # if version is vX.0 for a new X, then we need to find the highest v(X-1).Y:
  if [[ "$VERSION" =~ ^v[0-9]+\.0$ ]];
  then
    PREV_PREFIX=$(echo ${VERSION} | awk -F. '{print "v" substr($1, 2) - 1}')
    PREV_VERSION=$(git tag -l | grep -E $PREV_PREFIX |  grep -E "^v[0-9]+\.[0-9]+\.[0]$" | sort -V | tail -n 1)
  else
    PREV_VERSION=$(echo ${VERSION} | awk -F. -v OFS=. '{$NF -= 1 ; print}').0
  fi
  NOTES_ARG="--notes-start-tag ${PREV_VERSION}"
fi

if ! command -v gh &> /dev/null; then
  if [[ $OSTYPE == "darwin"* ]]; then
    echo "Installing github cli"
    brew install gh
  elif [[ $OSTYPE == "linux-gnu" ]]; then
    type -p yum-config-manager >/dev/null || sudo yum install yum-utils
    sudo yum-config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
    sudo yum -y install gh
  else
    echo "Please install github CLI: https://cli.github.com/"
    false
  fi
fi

GIT_VERSION=$(gh --version | perl -pe 'if(($v)=/([0-9]+([.][0-9]+)+)/){print"$v\n";exit}$_=""')
if ! { echo "2.28.0"; echo "$GIT_VERSION"; } | sort -V -C; then
  gh --version
  echo "You are running an out of date version of github cli. Please upgrade to at least v2.28.0"
  false
fi

BASE_REF=${3:-origin/main}

# Fetch origin/master, and confirm that this is OK
git fetch origin
git checkout $BASE_REF

git log -1
BRANCH=${VERSION}
if [[ "${CI}" = "false" ]]; then
  echo
  echo "We will create a new release branch '${BRANCH}' based on the above commit."
  echo

  read -p "Do you wish to continue? [Y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]
  then
    false
  fi
fi

# Fail if the release branch already exists
if git show-ref -q --heads origin/${BRANCH}; then
   echo "Release branch already exists at 'origin/${BRANCH}'"
   echo "Please checkout the '${BRANCH}' branch and use the following script to make hotfixes:"
   echo
   echo "  ./scripts/release/cherry_pick.sh <PULL_REQUEST>"
   echo
   false
fi

# Push the tag to github
TAG=${VERSION}.0
LATEST_TAG=${VERSION}

git checkout -b $BRANCH
git push origin $BRANCH
git tag $TAG
git push origin $TAG

# Make a new release
gh release create $TAG --verify-tag --generate-notes --title $TAG $NOTES_ARG

if [[ "$CI" = "false" ]]; then
  echo
  echo "Please run the following commands:"
  echo
  echo "  ./scripts/release/build_kumo_images.sh ${TAG}"
  echo "  ./scripts/release/build_kumo_images.sh ${LATEST_TAG}"
  echo
else
  echo "Building Kumo image on ${TAG}"
  ./scripts/release/build_kumo_images.sh ${TAG} "master" "saas snowflake databricks"
  ./scripts/release/build_kumo_images.sh ${LATEST_TAG} "master" "saas snowflake databricks"
fi
