#!/bin/bash
#
# Automatically squash and cherry-pick a PR onto the current branch.  This is
# useful for applying a hotfix to a release branch before the PR has been
# merged to master.
#

set -e

PULL_REQUEST=$1

if [[ $# -ne 1 ]]
then
  echo
  echo "Usage: ./scripts/release/cherry_pick.sh <PULL_REQUEST>"
  echo
  echo "  PULL_REQUEST: The ID of the pull request, such as '4320'"
  echo
  exit 1
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

# First make sure that the tree is clean
CHANGED_FILES=$(git diff HEAD)
if [[ ! -z "$CHANGED_FILES" ]]; then
  git status
  echo
  echo "There are changed files. Please commit or stash your changes"
  false
fi

VERSION=$(gh --version | perl -pe 'if(($v)=/([0-9]+([.][0-9]+)+)/){print"$v\n";exit}$_=""')
if ! { echo "2.28.0"; echo "$VERSION"; } | sort -V -C; then
  gh --version
  echo "You are running an out of date version of github cli. Please upgrade to at least v2.28.0"
  false
fi

# Ensure we are up to date with origin
git fetch

# Check if it has been merged
MERGED_AT=$(gh pr view $PULL_REQUEST --json mergedAt --template '{{.mergedAt}}')

if [[ "$MERGED_AT" != "<no value>" ]]; then
  # Case 1 -- the PR has already been merged
  COMMIT=$(gh pr view $PULL_REQUEST --json mergeCommit --template '{{.mergeCommit.oid}}')
  echo "PR has already been merged. Cherry-picking $COMMIT"
  git cherry-pick $COMMIT
else
  # Case 2 -- the PR is not merged, so we need to apply the patch manually
  echo "PR is not merged. Manually downloading and applying patch."

  # Write the diff to a temporary file
  PATCH_FILE=$(mktemp)
  echo "Writing diff to ${PATCH_FILE}"
  gh pr diff $PULL_REQUEST > $PATCH_FILE

  # Write the PR description to a temporary file
  DESCRIPTION_FILE=$(mktemp)
  echo "Writing description to ${DESCRIPTION_FILE}"
  gh pr view $PULL_REQUEST --json number,title,body,author --template \
  '{{printf "#%v" .number}} {{.title}}

{{.body}}

Author: {{.author.name}} @{{.author.login}}
' > $DESCRIPTION_FILE

  # Apply the patch
  set +e
  git apply --3way --index $PATCH_FILE
  if [ $? -ne 0 ]; then
    echo
    echo "Patch failed to apply cleanly. Please resolve conflicts and then run this command to commit:"
    echo
    echo "  git commit --file=${DESCRIPTION_FILE}"
    echo
    exit 1
  fi

  git commit --file=$DESCRIPTION_FILE
  if [ $? -ne 0 ]; then
    echo
    echo "Patch failed pre-commit checks. Please resolve error and then run this command to commit:"
    echo
    echo "  git commit --file=${DESCRIPTION_FILE}"
    echo
    exit 1
  fi
  set -e
fi

echo
echo "Hotfix was successful!"
echo
echo "To publish the hotfix release to GitHub, please run:"
echo
echo "    ./scripts/release/make_hotfix_release.sh"
