#!/bin/bash
#
# Tags the current commit as a hotfix, and generates a new release in Github,
# incrementing the minor version.
#
# This script must be run from the release branch, and the hotfixes should already
# be applied by using the cherry-pick.sh script.
#
# If this script fails, you will need to generate the hotfix manually. The
# instructions for manual release are here:
#
#    git tag vX.y.z
#    git push
#    git push origin vX.y.z
#    gh release create vX.y.z --verify-tag --generate-notes --title vX.Y.z --notes-start-tag vX.y.{z-1}
#
#    Alternatively, perform the last step in the UI: https://github.com/kumo-ai/kumo/releases/new

set -e

if [[ $# -gt 3 ]]
then
  echo
  echo "Usage: ./scripts/release/make_hotfix_release.sh <CI> <TAG> <PREV_TAG>"
  echo
  echo "  CI : Indicates that this script is run on CI."
  echo "  TAG (optional): The git tag for the release that will be created. "
  echo "    Defaults to PREV_TAG + 1"
  echo "  PREV_TAG (optional): The start tag that will be used to generate "
  echo "    release notes. All commits between PREV_TAG and TAG will be added "
  echo "    to the release notes."
  echo
  exit 1
fi

if ! command -v gh &> /dev/null; then
  if [[ $OSTYPE == "darwin"* ]]; then
    echo "Installing github cli"
    brew install gh
  else
    echo "Please install github CLI: https://cli.github.com/"
    false
  fi
fi

VERSION=$(gh --version | perl -pe 'if(($v)=/([0-9]+([.][0-9]+)+)/){print"$v\n";exit}$_=""')
if ! { echo "2.28.0"; echo "$VERSION"; } | sort -V -C; then
  gh --version
  echo "You are running an out of date version of github cli. Please upgrade to at least v2.28.0"
  false
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)
# TODO: Currently, the branch looks like heads/v1.41
# so we need to remove the heads/ prefix. This is needed
# if we need to handle a tag and a branch with the same
# name. Let's delete this once we fix the issue.
BRANCH=${BRANCH#heads/}
CI="${1:-false}"
TAG=$2
PREV_TAG=$3

if [ -z "$PREV_TAG" ];
then
  PREV_TAG=$(git tag | grep "^${BRANCH}" | grep -E "^v[1-9]+\.[0-9]+\.[0-9]+$" | sort -V | tail -1)

  if [[ ! "$PREV_TAG" =~ \.[0-9]+$ ]];
  then
    echo "Could not parse <PREV_TAG> from the branch. Expected to find tag matching '${BRANCH}.X'"
    echo "such as 'v1.9.4', but got '${PREV_TAG}'. Please manually specify CI, TAG and PREV_TAG"
    echo "on the command line:"
    echo
    echo "  ./scripts/release/make_hotfix_release.sh <CI> <TAG> <PREV_TAG>"
    false
  fi
fi

LATEST_TAG="${PREV_TAG%.*}"

if [ -z "$TAG" ];
  then
    TAG=$(echo ${PREV_TAG} | awk -F. -v OFS=. '{$NF += 1 ; print}')
fi

# Ensure that the local branch is up to date with the remote branch, in case
# someone else was pushing hotfixes
echo "Fetching latest changes from origin"
git fetch
git rebase origin/${BRANCH}

echo
echo "This will create a release tag '${TAG}' with the following hotfixes:"
echo

CHANGES=$(git log ${PREV_TAG}..HEAD --oneline)

if [[ -z "$CHANGES" ]]; then
  echo "  No hotfixes were found since version '${PREV_TAG}'"
else
  echo "${CHANGES}"
fi

if [[ "${CI}" = "false" ]]; then
  echo
  echo "The release will be pushed to branch 'origin/${BRANCH}' and the previous "
  echo "tag '${PREV_TAG}' will be used to generate release notes."
  echo
  echo "If this is not correct, please manually specify the <CI>, <TAG> and <PREV_TAG> "
  echo "when running this script:"
  echo
  echo "  ./scripts/release/make_hotfix_release.sh <CI> <TAG> <PREV_TAG>"
  echo
  echo
  read -p "Do you wish to continue? [Y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]
  then
    false
  fi
fi

# Push the tag and create the release
git tag $TAG
git push origin $TAG

gh release create $TAG --verify-tag --title $TAG --notes "$CHANGES"

if [[ "${CI}" = "false" ]]; then
  echo
  echo "Please run the following commands:"
  echo
  echo "  ./scripts/release/build_kumo_images.sh ${TAG}"
  echo "  ./scripts/release/build_kumo_images.sh ${LATEST_TAG}"
  echo
else
  echo "Building kumo images"
  ./scripts/release/build_kumo_images.sh ${TAG} "master" "saas snowflake databricks"
  ./scripts/release/build_kumo_images.sh ${LATEST_TAG} "master" "saas snowflake databricks"
fi
