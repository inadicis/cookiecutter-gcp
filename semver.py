import argparse
import re
import shutil
import subprocess
from pathlib import Path

import pytest
import toml

# TODO have option to get version from a version.py file instead of pyproject.toml?
#   or can specify what sub-part of the pyproject.toml ?
# TODO have a pydantic model like Settings for the pyproject.toml?
# TODO handle when no pyproject yet / no version yet -> 0.0.1 ?

# TODO automated testing?
# TODO manual testing params -r, -P, -t

# TODO tag prefix as param / option? as env variable?
# TODO make semver not a string to make it mutable ?  (not re-instantiate one for each bump)

# TODO make this a package, pip installable

parser = argparse.ArgumentParser(
    description="Script to upgrade the version of the project, both in the code and in git tags. "
                "Assumes the repo to have a pyproject.toml at root with top level field `version."
                "This version must be` a string following semantic version syntax "
                "(without `+` suffix, only `-` suffix are allowed). \n"
                "Requires git to be installed and accessible via command `git`"
)

group_version = parser.add_mutually_exclusive_group(required=True)
group_version.add_argument(
    "version",
    nargs="?",
    help="Semantic version to be used to update project and tag git.\n"
         "Required if params -p, -m and -M not used.",
    default=None
)
group_version.add_argument(
    "-p", "--patch",
    help="Increment version's patch number",
    action="store_true"
)
group_version.add_argument(
    "-m", "--minor",
    help="Increment version's minor number",
    action="store_true"
)
group_version.add_argument(
    "-M", "--major",
    help="Increment version's major number",
    action="store_true"
)

parser.add_argument(
    "-c", "--metadata", "--comment",
    help="Add semver suffix after a dash ``-``. Can be alphanumeric with dashes",
    default=None
)

parser.add_argument(
    "--tag-prefix",
    help="A prefix for the git tag",
    default=""
)

parser.add_argument(
    "-t", "--test",
    help="Whether to check if tests run. Expects directory \"tests\" at repo root",
    action="store_true"
)

parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-P", "--push", help="Push commit and tag to origin", action="store_true")
parser.add_argument(
    "-r", "--repo",
    help="Path to the root of the repository. Defaults to current working directory",
    default="."
)
parser.add_argument(
    "-T", "--table",
    help="TOML table where to find version.",
    default="project"
)

GIT = shutil.which("git")


class SemanticVersion(str):
    """
    semantic version validation but keeping it as a string.
    It does not exactly follow https://semver.org/ specification
    as the two metadata fields are
    merged together (the character "+" cannot be used)
    """

    def __new__(cls, string="0.0.1"):
        if not isinstance(string, str):
            raise TypeError("string required")

        match = re.match(
            r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
            r"(-(0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))?$",
            string,

        )
        if match is None:
            raise ValueError("Not valid semantic version")
        return super().__new__(cls, string)

    def __repr__(self):
        return f"SemVer({super().__repr__()})"

    @property
    def major(self) -> int:
        return int(self.split(".")[0])

    @property
    def minor(self) -> int:
        return int(self.split(".")[1])

    @property
    def patch(self) -> int:
        minor, *comments = self.split(".")[2].split('-')
        return int(minor)

    @property
    def metadata(self) -> str:
        """
        This is a mix of semver's prerelease and build metadata,
        as the "+" character is not allowed
        """
        minor, *comments = self.split(".")[2].split('-')
        return "-".join(comments)

    def next_patch(self) -> "Self":
        return type(self)(f"{self.major}.{self.minor}.{self.patch + 1}")

    def next_minor(self) -> "Self":
        return type(self)(f"{self.major}.{self.minor + 1}.0")

    def next_major(self) -> "Self":
        return type(self)(f"{self.major + 1}.0.0")

    def add_metadata(self, comment) -> "Self":
        return type(self)(f"{self}-{comment}")


def main():
    args = parser.parse_args()

    root_dir = Path(args.repo)
    pyproject_path = root_dir / 'pyproject.toml'

    if args.verbose:
        print(f"Using Repo at: {root_dir}")

    if args.test:
        exit_code = pytest.main(root_dir / "tests")
        if exit_code != 0:
            print(
                "The test pipeline did not work. Make sure all tests passed successfully before "
                "tagging"
            )
            return

    with open(pyproject_path, 'r') as f:
        project_settings = toml.loads(f.read())

    old_version: str = project_settings[args.table]["version"]

    if args.verbose:
        print(f"Previous version read from pyproject.toml: {old_version}")

    old_semver = SemanticVersion(old_version)

    if args.version is not None:
        new_semver = SemanticVersion(args.version)
    elif args.patch:
        new_semver = old_semver.next_patch()
    elif args.minor:
        new_semver = old_semver.next_minor()
    elif args.major:
        new_semver = old_semver.next_major()
    else:
        raise ValueError("This should not be reachable.")

    if args.metadata is not None:
        new_semver = new_semver.add_metadata(args.metadata)

    new_version = str(new_semver)

    project_settings[args.table]["version"] = new_version

    if args.verbose:
        print(f"New version: {new_version}")

    with open(pyproject_path, 'w') as f:
        toml.dump(project_settings, f)

    if args.verbose:
        print(f"Updated version in pyproject.toml")

    subprocess.call([GIT, "add", str(pyproject_path)])
    subprocess.call([GIT, "commit", "-m", f"Update version to {new_version}"])
    if args.verbose:
        print(f"Committed new version")

    tag = f"{args.tag_prefix}{new_semver}"
    subprocess.call([GIT, "tag", "-a", tag, "-m", f"Update version to {new_version}"])
    if args.verbose:
        print(f"Created tag: {tag}")

    if args.push:
        subprocess.call([GIT, "push"])
        subprocess.call([GIT, "push", "origin", tag])
        if args.verbose:
            print(f"Pushed commit + tag: {tag} to origin")


if __name__ == '__main__':
    main()
