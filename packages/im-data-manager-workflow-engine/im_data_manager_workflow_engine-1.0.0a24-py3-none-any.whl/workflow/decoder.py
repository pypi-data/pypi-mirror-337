"""A module to validate and decode workflow definitions.

This is typically used by the Data Manager's Workflow Engine.
"""

import os
from typing import Any

import jsonschema
import yaml

# The (built-in) schemas...
# from the same directory as us.
_WORKFLOW_SCHEMA_FILE: str = os.path.join(
    os.path.dirname(__file__), "workflow-schema.yaml"
)

# Load the Workflow schema YAML file now.
# This must work as the file is installed along with this module.
assert os.path.isfile(_WORKFLOW_SCHEMA_FILE)
with open(_WORKFLOW_SCHEMA_FILE, "r", encoding="utf8") as schema_file:
    _WORKFLOW_SCHEMA: dict[str, Any] = yaml.load(schema_file, Loader=yaml.FullLoader)
assert _WORKFLOW_SCHEMA


def validate_schema(workflow: dict[str, Any]) -> str | None:
    """Checks the Workflow Definition against the built-in schema.
    If there's an error the error text is returned, otherwise None.
    """
    assert isinstance(workflow, dict)

    try:
        jsonschema.validate(workflow, schema=_WORKFLOW_SCHEMA)
    except jsonschema.ValidationError as ex:
        return str(ex.message)

    # OK if we get here
    return None


def get_step_names(definition: dict[str, Any]) -> list[str]:
    """Given a Workflow definition this function returns the list of
    step names, in the order they are defined.
    """
    names: list[str] = [step["name"] for step in definition.get("steps", [])]
    return names


def get_steps(definition: dict[str, Any]) -> list[dict[str, Any]]:
    """Given a Workflow definition this function returns the steps."""
    response: list[dict[str, Any]] = definition.get("steps", [])
    return response


def get_name(definition: dict[str, Any]) -> str:
    """Given a Workflow definition this function returns its name."""
    return str(definition.get("name", ""))


def get_description(definition: dict[str, Any]) -> str | None:
    """Given a Workflow definition this function returns its description (if it has one)."""
    return definition.get("description")


def get_variable_names(definition: dict[str, Any]) -> list[str]:
    """Given a Workflow definition this function returns all the names of the
    variables defined at the workflow level."""
    wf_variable_names: set[str] = set()
    variables: dict[str, Any] | None = definition.get("variables")
    if variables:
        for input_variable in variables.get("inputs", []):
            name: str = input_variable["name"]
            assert name not in wf_variable_names
            wf_variable_names.add(name)
    return list(wf_variable_names)
