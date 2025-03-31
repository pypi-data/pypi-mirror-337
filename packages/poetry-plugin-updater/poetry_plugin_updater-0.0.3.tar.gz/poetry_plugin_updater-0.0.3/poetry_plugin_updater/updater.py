from __future__ import annotations

import string
import typing

import requests

if typing.TYPE_CHECKING:
    from tomlkit import TOMLDocument

PYPI_URL_TEMPLATE = "https://pypi.org/pypi/%(project)s/json"


def get_updated_version(project: str, version: str) -> str:
    if version == "*":
        return version

    for i, c in enumerate(version):
        if c in string.digits:
            index = i
            break
    else:
        raise ValueError(f"Cannot parse `{version}`.")

    latest_version = requests.get(PYPI_URL_TEMPLATE % {"project": project}).json()["info"]["version"]
    return f"{version[:index]}{latest_version}"


def update_dependency(project: str, version_or_dict: str | dict[str, typing.Any]) -> str | dict[str, typing.Any]:
    if isinstance(version_or_dict, str):
        return get_updated_version(project, version_or_dict)
    else:
        if "version" not in version_or_dict:
            return version_or_dict
        return version_or_dict | {"version": get_updated_version(project, version_or_dict["version"])}


def update_dependencies_group(deps: dict[str, typing.Any]) -> None:
    for project in list(deps.keys()):
        if project == "python":
            continue

        project_metadata = deps[project]
        if isinstance(project_metadata, list):
            for i, item in enumerate(project_metadata):
                deps[project][i] = update_dependency(project, item)
        else:
            deps[project] = update_dependency(project, project_metadata)


def update_pyproject_file(pyproject_file: TOMLDocument) -> None:
    poetry_content = pyproject_file["tool"]["poetry"]

    update_dependencies_group(poetry_content["dependencies"])
    for group, group_data in poetry_content.get("group", {}).items():
        if dependencies := group_data.get("dependencies"):
            update_dependencies_group(dependencies)
