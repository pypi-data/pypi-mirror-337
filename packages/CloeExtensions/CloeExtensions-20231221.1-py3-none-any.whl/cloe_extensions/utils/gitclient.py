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
        regex and transforms yaml to dict.

        Args:
            file_path (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            dict: _description_
        """
        commit_start = self._get_commit_from_tag()
        git_cmd = f"{commit_start}:{file_path.as_posix()}"
        return yaml.safe_load(self.repository.git.show(git_cmd))
