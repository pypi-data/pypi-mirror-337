"""Module keeps all git related classes and methods.
"""
import json
import logging
import pathlib
import re

import git
import yaml
from git.objects import Commit

logger = logging.getLogger(__name__)


class GitClient:
    """
    Client for any operation regarding the underlying git repository
    """

    def __init__(self, model_root_path: pathlib.Path, git_tag_regex: str) -> None:
        """
            Inits a new git client.
        Args:
            model_root_path: str - root path of git repo
            git_tag_regex: str - regular expression by which to find the
            starting commit
        """
        self.git_tag_regex = git_tag_regex
        self.model_root_path = model_root_path
        self.repository = git.Repo(str(self.model_root_path))

    def _get_commit_from_tag(self) -> Commit:
        """Evaluates the changes found in the solution git repository
        and returns a collection of changes with meta information.

        Will take latest commit that matches git_tag_regex as first commit.
        Will take current commit as last commit.

        Raises:
            ValueError: _description_

        Returns:
            dict: _description_
        """
        tags_sorted = sorted(
            self.repository.tags, key=lambda t: t.commit.committed_datetime
        )
        commit_start: Commit | None = None
        for tag in reversed(tags_sorted):
            if re.search(self.git_tag_regex, tag.name):
                commit_start = tag.commit
                break
        if commit_start is None:
            logger.error(
                "Git mode requires at least one tag with format [ '%s' ]",
                self.git_tag_regex,
            )
            raise ValueError(
                (
                    "Git mode requires at least one tag with"
                    f" format [ '{self.git_tag_regex}' ]"
                )
            )
        logger.info("Commit found: %s", commit_start)
        return commit_start

    def get_json_from_tag(self, file_path: pathlib.Path) -> dict:
        """Wrapper function for _get_commit_from_tag. Gets commit based on
        regex and transforms json to dict.

        Args:
            file_path (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            dict: _description_
        """
        commit_start = self._get_commit_from_tag()
        git_cmd = f"{commit_start}:{file_path.as_posix()}"
        return json.loads(self.repository.git.show(git_cmd))

    def get_yaml_from_tag(self, file_path: pathlib.Path) -> dict | None:
        """Wrapper function for _get_commit_from_tag. Gets commit based on
        regex and transforms yaml to dict or combines multiple yaml files in a directory.

        Args:
            file_path (pathlib.Path): Path to a yaml file or a directory within the Git history.

        Raises:
            ValueError: If the path is invalid or other Git errors occur.

        Returns:
            dict: Dictionary representation of the yaml file(s).
        """
        commit_start = self._get_commit_from_tag()
        combined_yaml = {}

        # Retrieve list of files at the specified commit
        git_file_list = self.repository.git.ls_tree(commit_start, r=True).split("\n")
        git_files = [line.split("\t")[1] for line in git_file_list if line]

        # Check if the path is a directory or a file in the context of Git history
        is_dir = any(f.startswith(file_path.as_posix()) for f in git_files)
        is_file = file_path.as_posix() in git_files

        if is_dir:
            # Handle directory containing multiple YAML files
            for git_file in git_files:
                if git_file.startswith(file_path.as_posix()) and (
                    git_file.endswith(".yaml") or git_file.endswith(".yml")
                ):
                    git_cmd = f"{commit_start}:{git_file}"
                    file_content = yaml.safe_load(self.repository.git.show(git_cmd))
                    combined_yaml.update(file_content)
        elif is_file:
            # Handle a single YAML file
            git_cmd = f"{commit_start}:{file_path.as_posix()}"
            combined_yaml = yaml.safe_load(self.repository.git.show(git_cmd))
        else:
            raise ValueError(
                "Provided path is neither a file nor a directory in the Git history"
            )

        return combined_yaml
