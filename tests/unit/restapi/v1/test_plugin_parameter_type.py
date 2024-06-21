# This Software (Dioptra) is being made available as a public service by the
# National Institute of Standards and Technology (NIST), an Agency of the United
# States Department of Commerce. This software was developed in part by employees of
# NIST and in part by NIST contractors. Copyright in portions of this software that
# were developed by NIST contractors has been licensed or assigned to NIST. Pursuant
# to Title 17 United States Code Section 105, works of NIST employees are not
# subject to copyright protection in the United States. However, NIST may hold
# international copyright in software created by its employees and domestic
# copyright (or licensing rights) in portions of software that were assigned or
# licensed to NIST. To the extent that NIST holds copyright in this software, it is
# being made available under the Creative Commons Attribution 4.0 International
# license (CC BY 4.0). The disclaimers of the CC BY 4.0 license apply to all parts
# of the software developed or licensed by NIST.
#
# ACCESS THE FULL CC BY 4.0 LICENSE HERE:
# https://creativecommons.org/licenses/by/4.0/legalcode
"""Test suite for plugin paramaeter type operations.

This module contains a set of tests that validate the CRUD operations and additional
functionalities for the plugin paramaeter type entity. The tests ensure that the plugin
paramaeter types can be submitted and retrieved as expected through the REST API.
"""
from typing import Any

import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from werkzeug.test import TestResponse

from dioptra.restapi.routes import V1_PLUGIN_PARAMETER_TYPES_ROUTE, V1_ROOT

from ..lib import actions, helpers

# -- Actions ---------------------------------------------------------------------------


def modify_plugin_parameter_type(
    client: FlaskClient,
    id: int,
    new_name: str,
    new_structure: dict[str, Any] | None = None,
    new_description: str | None = None,
) -> TestResponse:
    """Rename a Plugin Parameter Type using the API.

    Args:
        client: The Flask test client.
        id: The id of the plugin parameter type to rename.
        new_name: The new name to assign to the plugin parameter type.
        new_structure: The new structure to assign to the plugin parameter type.
        new_description: The new description to assign to the plugin parameter type.

    Returns:
        The response from the API.
    """
    json_payload = {"name": new_name}

    if new_structure is not None:
        json_payload["structure"] = new_structure

    if new_description is not None:
        json_payload["description"] = new_description
    print("MODIFY", json_payload)

    return client.put(
        f"/{V1_ROOT}/{V1_PLUGIN_PARAMETER_TYPES_ROUTE}/{id}",
        json=json_payload,
        follow_redirects=True,
    )


def delete_plugin_parameter_type_with_id(client: FlaskClient, id: int) -> TestResponse:
    """Delete a plugin parameter type using the API.

    Args:
        client: The Flask test client.
        id: The id of the plugin parameter type to delete.

    Returns:
        The response from the API.
    """
    return client.delete(
        f"/{V1_ROOT}/{V1_PLUGIN_PARAMETER_TYPES_ROUTE}/{id}",
        follow_redirects=True,
    )


# -- Assertions ------------------------------------------------------------------------


def assert_retrieving_plugin_parameter_types_works(
    client: FlaskClient,
    expected: list[dict[str, Any]],
    group_id: int | None = None,
    search: str | None = None,
    paging_info: dict[str, Any] | None = None,
) -> None:
    """Assert that retrieving plugin parameter types works.

    Args:
        client: The Flask test client.
        expected: The expected response from the API.
        group_id: The group of the plugin parameter type.
        search: The search query parameters.
        paging_info: The paging query parameters.

    Raises:
        AssertionError: If the response status code is not 200 or if the API response
            does not match the expected response.
    """

    query_string: dict[str, Any] = {}

    # if group_id:
    query_string["group_id"] = group_id

    if search is not None:
        query_string["search"] = search

    if paging_info is not None:
        query_string["index"] = paging_info["index"]
        query_string["pageLength"] = paging_info["page_length"]

    response = client.get(
        f"/{V1_ROOT}/{V1_PLUGIN_PARAMETER_TYPES_ROUTE}",
        query_string=query_string,
        follow_redirects=True,
    )
    assert response.status_code == 200 and response.get_json()["data"] == expected


def assert_retrieving_plugin_parameter_type_by_id_works(
    client: FlaskClient, id: int, expected: dict[str, Any]
) -> None:
    """Assert that retrieving a plugin parameter type by id works.

    Args:
        client: The Flask test client.
        id: The id of the plugin parameter type to retrieve.
        expected: The expected response from the API.

    Raises:
        AssertionError: If the response status code is not 200 or if the API response
            does not match the expected response.
    """
    response = client.get(
        f"/{V1_ROOT}/{V1_PLUGIN_PARAMETER_TYPES_ROUTE}/{id}", follow_redirects=True
    )
    assert response.status_code == 200 and response.get_json() == expected


def assert_plugin_parameter_type_name_matches_expected_name(
    client: FlaskClient, id: int, expected_name: str
) -> None:
    """Assert that the name of a plugin parameter type matches the expected name.

    Args:
        client: The Flask test client.
        id: The id of the plugin parameter type to retrieve.
        expected_name: The expected name of the plugin parameter type.

    Raises:
        AssertionError: If the response status code is not 200 or if the name of the
            experiment does not match the expected name.
    """
    response = client.get(
        f"/{V1_ROOT}/{V1_PLUGIN_PARAMETER_TYPES_ROUTE}/{id}",
        follow_redirects=True,
    )
    assert response.status_code == 200 and response.get_json()["name"] == expected_name


def assert_updating_plugin_parameter_type_works(
    client: FlaskClient, id: int, expected: dict[str, Any]
) -> None:
    """Assert that updating a plugin parameter type by id works.

    Args:
        client: The Flask test client.
        id: The id of the plugin parameter type to retrieve.
        expected: The expected response from the API.

    Raises:
        AssertionError: If the response status code is not 200 or if the API response
            does not match the expected response.
    """
    response = client.put(
        f"/{V1_ROOT}/{V1_PLUGIN_PARAMETER_TYPES_ROUTE}/{id}", follow_redirects=True
    )
    assert response.status_code == 200 and response.get_json() == expected


def assert_deleting_plugin_parameter_type_by_id_works(
    client: FlaskClient, id: int, expected: dict[str, Any]
) -> None:
    """Assert that deleting a plugin parameter type by id works.

    Args:
        client: The Flask test client.
        id: The id of the plugin parameter type to delete.
        expected: The expected response from the API.

    Raises:
        AssertionError: If the response status code is not 404 or if the API response
            does not match the expected response.
    """
    response = client.delete(
        f"/{V1_ROOT}/{V1_PLUGIN_PARAMETER_TYPES_ROUTE}/{id}", follow_redirects=True
    )
    assert response.status_code == 200 and response.get_json() == expected


def assert_plugin_parameter_type_is_not_found(client: FlaskClient, id: int) -> None:
    """Assert that a plugin parameter type is not found.

    Args:
        client: The Flask test client.
        id: The id of the plugin parameter type to retrieve.

    Raises:
        AssertionError: If the response status code is not 404.
    """
    response = client.get(
        f"/{V1_ROOT}/{V1_PLUGIN_PARAMETER_TYPES_ROUTE}/{id}",
        follow_redirects=True,
    )
    assert response.status_code == 404


def assert_cannot_rename_invalid_plugin_parameter_type(
    client: FlaskClient, id: int, json_payload: dict[str, Any]
) -> None:
    """Assert that attempting to rename a Plugin Parameter Type with invalid
    parameters using the API fails.

    Args:
        client: The Flask test client.
        id: The id of the plugin parameter type to rename.
        json_payload: The full payload to be sent to the API.

    Raises:
        AssertionError: If the response status code is not 400.
    """
    response = client.put(
        f"/{V1_ROOT}/{V1_PLUGIN_PARAMETER_TYPES_ROUTE}/{id}",
        json=json_payload,
        follow_redirects=True,
    )
    assert response.status_code == 400


def assert_cannot_create_invalid_plugin_parameter_type(
    client: FlaskClient, json_payload: dict[str, Any]
) -> None:
    """Assert that attempting to create a Plugin Parameter Type with invalid
    parameters using the API fails.

    Args:
        client: The Flask test client.
        json_payload: The full payload to be sent to the API.

    Raises:
        AssertionError: If the response status code is not 400.
    """
    response = client.post(
        f"/{V1_ROOT}/{V1_PLUGIN_PARAMETER_TYPES_ROUTE}",
        json=json_payload,
        follow_redirects=True,
    )
    assert response.status_code == 400


def assert_cannot_create_existing_plugin_parameter_type(
    client: FlaskClient, name: str, group_id: int
) -> None:
    """Assert that attempting to create a Plugin Parameter Type with an existing
    name using the API fails.

    Args:
        client: The Flask test client.
        name: The name of the plugin parameter type.
        group_id: The group of the plugin parameter type.

    Raises:
        AssertionError: If the response status code is not 400.
    """
    response = actions.register_plugin_parameter_type(
        client, name=name, group_id=group_id, structure=dict(), description=""
    )
    assert response.status_code == 400


def assert_cannot_rename_plugin_parameter_type_to_existing_name(
    client: FlaskClient,
    id: int,
    existing_name: str,
    new_structure: dict[str, Any],
    new_description: str,
) -> None:
    """Assert that attempting to rename a Plugin Parameter Type to an existing
    name using the API fails.

    Args:
        client: The Flask test client.
        id: The id of the plugin parameter type to rename.
        existing_name: The name of an existing plugin parameter type.
        new_structure: The new structure to assign to the plugin parameter type.

    Raises:
        AssertionError: If the response status code is not 400.
    """
    response = modify_plugin_parameter_type(
        client,
        id=id,
        new_name=existing_name,
        new_structure=new_structure,
        new_description=new_description,
    )
    assert response.status_code == 400


def assert_cannot_delete_invalid_plugin_parameter_type(
    client: FlaskClient, id: Any, json_payload: dict[str, Any]
) -> None:
    """Assert that attempting to delete a Plugin Parameter Type with invalid
    parameters using the API fails.

    Args:
        client: The Flask test client.
        id: The id of the plugin parameter type to delete.
        json_payload: The full payload to be sent to the API.

    Raises:
        AssertionError: If the response status code is not 400.
    """
    response = client.delete(
        f"/{V1_ROOT}/{V1_PLUGIN_PARAMETER_TYPES_ROUTE}/{id}",
        json=json_payload,
        follow_redirects=True,
    )
    assert response.status_code == 400


def assert_plugin_parameter_type_content_matches_expectations(
    response: dict[str, Any], expected_contents: dict[str, Any]
) -> None:
    """Assert that a Plugin Parameter Type's fields match the expected values.

    Args:
        response: The response to check.
        expected_contents: The expected values for the response.
    """
    expected_keys = {
        "id",
        "snapshot",
        "group",
        "user",
        "createdOn",
        "lastModifiedOn",
        "latestSnapshot",
        "hasDraft",
        "name",
        "structure",
        "description",
        "tags",
    }
    assert set(response.keys()) == expected_keys

    # Validate the non-Ref fields
    assert isinstance(response["id"], int)
    assert isinstance(response["snapshot"], int)
    assert isinstance(response["name"], str)
    assert isinstance(response["structure"], (dict, type(None)))
    assert isinstance(response["description"], (str, type(None)))
    assert isinstance(response["createdOn"], str)
    assert isinstance(response["lastModifiedOn"], str)
    assert isinstance(response["latestSnapshot"], bool)
    assert isinstance(response["hasDraft"], bool)

    assert response["name"] == expected_contents["name"]
    assert response["structure"] == expected_contents["structure"]
    assert response["description"] == expected_contents["description"]

    assert helpers.is_iso_format(response["createdOn"])
    assert helpers.is_iso_format(response["lastModifiedOn"])

    # Validate the UserRef structure
    assert isinstance(response["user"]["id"], int)
    assert isinstance(response["user"]["username"], str)
    assert isinstance(response["user"]["url"], str)
    assert response["user"]["id"] == expected_contents["user_id"]

    # Validate the GroupRef structure
    assert isinstance(response["group"]["id"], int)
    assert isinstance(response["group"]["name"], str)
    assert isinstance(response["group"]["url"], str)
    assert response["group"]["id"] == expected_contents["group_id"]


# -- Tests -----------------------------------------------------------------------------


def test_get_all_plugin_parameter_types(
    client: FlaskClient,
    db: SQLAlchemy,
    auth_account: dict[str, Any],
    registered_plugin_parameter_types: dict[str, Any],
) -> None:
    """Test that all Plugin Parameter Types can be retrieved.

        Scenario: Get a List of Plugin Parameter Types
            Given I am an authorized user,
            I need to be able to submit a GET request with optional query parameters
            in order to retrieve a list of plugin parameter types matching the
            parameters.

    This test validates this scenario by following these actions:

    - The user is able to retrieve a list of all plugin parameter types.
    - The returned list of plugin parameter types match the full list of existing plugin
      parameter types.
    """
    plugin_param_type_expected_list = list(registered_plugin_parameter_types.values())
    assert_retrieving_plugin_parameter_types_works(
        client, expected=plugin_param_type_expected_list
    )


@pytest.mark.v1_test
def test_plugin_parameter_type_search_query(
    client: FlaskClient,
    db: SQLAlchemy,
    auth_account: dict[str, Any],
    registered_plugin_parameter_types: dict[str, Any],
) -> None:
    """Test that multiple Plugin Parameter Types can be retrieved using search terms.

    Given an authenticated user and registered plugin parameter types, this test
    validates this scenario by following these actions:

    - The user is able to retrieve 2 lists of the submitted plugin parameter types
      using different query parameters.
    - The returned lists of plugin parameter types match the searches provided
      during both submissions.
    """
    plugin_param_type_expected_list = list(registered_plugin_parameter_types.values())[
        :2
    ]
    search_parameters = "name:*int*"
    assert_retrieving_plugin_parameter_types_works(
        client, expected=plugin_param_type_expected_list, search=search_parameters
    )

    plugin_param_type_expected_list2 = registered_plugin_parameter_types[
        "plugin_param_type3"
    ]
    search_parameters = "name:*str*"
    assert_retrieving_plugin_parameter_types_works(
        client, expected=plugin_param_type_expected_list2, search=search_parameters
    )


def test_plugin_parameter_type_group_query(
    client: FlaskClient,
    db: SQLAlchemy,
    auth_account: dict[str, Any],
    registered_plugin_parameter_types: dict[str, Any],
) -> None:
    """Test that Plugin Parameter Types can be retrieved using a group filter.

    Given an authenticated user and registered plugin parameter types, this test
    validates this scenario by following these actions:

    - The user is able to retrieve a list of all submitted plugin parameter types
      owned by the default group.
    - The returned list of plugin parameter types matches the expected list owned by
      the default group.
    """
    plugin_param_type_expected_list = list(registered_plugin_parameter_types.values())
    assert_retrieving_plugin_parameter_types_works(
        client,
        expected=plugin_param_type_expected_list,
        group_id=auth_account["groups"][0]["id"],
    )


def test_create_plugin_parameter_type(
    client: FlaskClient, db: SQLAlchemy, auth_account: dict[str, Any]
) -> None:
    """Test that Plugin Parameter Types can be created using the API.

        Scenario: Create a Plugin Parameter Type
            Given I am an authorized user,
            I need to be able to submit a POST request with body parameters name
            group_id, and optional structure
            in order to create a new plugin parameter type.

    This test validates the following sequence of actions:
    - A user submits a POST request for a plugin parameter type.
    - The user retrieves information about one plugin parameter type using its id.
    - The returned information matches what was provided during creation.
    - This set of steps is repeated when testing using a missing parameter, extra
      parameter and a parameter with the wrong type during the POST request.
    - The second, third and fourth POST operations are expected to fail.
    """
    name = "test_plugin_param_type"
    user_id = auth_account["id"]
    group_id = auth_account["groups"][0]["id"]
    description = "This is a plugin parameter type"
    plugin_param_type1_response = actions.register_plugin_parameter_type(
        client,
        name=name,
        group_id=group_id,
        description=description,
    )
    plugin_param_type1_expected = plugin_param_type1_response.get_json()
    assert_plugin_parameter_type_content_matches_expectations(
        response=plugin_param_type1_expected,
        expected_contents={
            "name": name,
            "user_id": user_id,
            "group_id": group_id,
            "description": description,
            "structure": None,
        },
    )
    assert_retrieving_plugin_parameter_type_by_id_works(
        client,
        id=plugin_param_type1_expected["id"],
        expected=plugin_param_type1_expected,
    )

    # Error case (missing parameter)
    assert_cannot_create_invalid_plugin_parameter_type(client, json_payload={})

    # Error case (extra parameter)
    assert_cannot_create_invalid_plugin_parameter_type(
        client,
        json_payload={
            "name": "plugin_param_type_2",
            "extra_param": "invalid",
            "extra_param2": "invalid2",
        },
    )

    # Error case (wrong type)
    assert_cannot_create_invalid_plugin_parameter_type(
        client,
        json_payload={
            "name": "plugin_param_type_1",
            "group_id": "invalid",
        },
    )


def test_get_plugin_parameter_type(
    client: FlaskClient,
    db: SQLAlchemy,
    auth_account: dict[str, Any],
    registered_plugin_parameter_types: dict[str, Any],
) -> None:
    """Test that a Plugin Parameter Type can be retrieved following the scenario below:

        Scenario: Get a Plugin Parameter Type using its ID
            Given I am an authorized user and at least one plugin parameter type exists,
            I need to be able to submit a GET request with path parameter id
            in order to retrieve the plugin parameter type with the specified ID.

    This test validates this scenario by following these actions:

    - A user submits a POST request for two plugin parameter types.
    - The user retrieves information about one plugin parameter type using its id.
    - The returned information matches what was provided during creation.
    """
    plugin_param_type1_expected = registered_plugin_parameter_types[
        "plugin_param_type1"
    ]

    # Get a Plugin Parameter Type using its ID
    assert_retrieving_plugin_parameter_type_by_id_works(
        client,
        id=plugin_param_type1_expected["id"],
        expected=plugin_param_type1_expected,
    )


def test_delete_plugin_parameter_type(
    client: FlaskClient,
    db: SQLAlchemy,
    auth_account: dict[str, Any],
    registered_plugin_parameter_types: dict[str, Any],
) -> None:
    """Test that a Plugin Parameter Type can be deleted following the scenario below:

         Scenario: Delete a Plugin Parameter Type
              Given I am an authorized user and at least one plugin parameter type
              exists, I need to be able to submit a DELETE request with path parameter
              id in order to delete a plugin parameter type with the specified ID.

    This test validates these scenarios by following these actions:

     - A user submits a POST request for two plugin parameter types.
     - The user retrieves information about one plugin parameter type using its id.
     - The returned information matches what was provided during creation.
     - The plugin parameter type is then deleted.
     - A search by id for the deleted plugin parameter type should return a 404 error.
    """
    plugin_param_type1 = registered_plugin_parameter_types["plugin_param_type1"]

    # Delete a Plugin Parameter Type using its ID
    assert_retrieving_plugin_parameter_type_by_id_works(
        client, id=plugin_param_type1["id"], expected=plugin_param_type1
    )
    delete_plugin_parameter_type_with_id(client, plugin_param_type1["id"])
    assert_plugin_parameter_type_is_not_found(client, plugin_param_type1["id"])


def test_modify_plugin_parameter_type(
    client: FlaskClient,
    db: SQLAlchemy,
    auth_account: dict[str, Any],
    registered_plugin_parameter_types: dict[str, Any],
) -> None:
    """Test that a Plugin Parameter Type can be modified following the scenario below:

        Scenario: Modify an Existing Plugin Parameter Type
            Given I am an authorized user and at least one plugin parameter type exists,
            I need to be able to submit a PUT request with path parameter id and body
            parameters name and structure in order to update the plugin parameter type
            with the new name and structure parameters.

    This test validates this scenario by following these actions:

    - A user creates a plugin parameter type.
    - The user is able to retrieve information about the plugin parameter type that
      matches the information that was provided during creation.
    - The user modifies this same plugin parameter type.
    - The user retrieves information about the same plugin parameter type and it
      reflects the changes.
    - A user then attempts to modify a plugin parameter type with a missing parameter,
      extra parameter, and a parameter with the wrong type in the request.
    - Each of these cases causes an error to be returned.
    """
    plugin_param_type1 = registered_plugin_parameter_types["plugin_param_type1"]
    plugin_param_type2 = registered_plugin_parameter_types["plugin_param_type2"]
    plugin_param_type3 = registered_plugin_parameter_types["plugin_param_type3"]

    start_name = plugin_param_type1["name"]
    updated_name = "changed_name"
    updated_structure = {"key": "value"}

    # Modify an Existing Plugin Parameter Type
    assert_plugin_parameter_type_name_matches_expected_name(
        client, id=plugin_param_type1["id"], expected_name=start_name
    )
    modify_plugin_parameter_type(
        client,
        id=plugin_param_type1["id"],
        new_name=updated_name,
        new_structure=updated_structure,
        new_description=plugin_param_type1["description"],
    )
    assert_plugin_parameter_type_name_matches_expected_name(
        client, id=plugin_param_type1["id"], expected_name=updated_name
    )

    # Error case (missing parameter)
    assert_cannot_rename_invalid_plugin_parameter_type(
        client, id=plugin_param_type2["id"], json_payload={}
    )

    # Error case (extra parameter)
    assert_cannot_rename_invalid_plugin_parameter_type(
        client,
        id=plugin_param_type2["id"],
        json_payload={
            "name": "param_name",
            "extra_param": "invalid",
        },
    )

    # Error case (wrong type)
    assert_cannot_rename_invalid_plugin_parameter_type(
        client,
        id=plugin_param_type2["id"],
        json_payload={"name": 42, "structure": dict()},
    )

    # Attempt to rename a Plugin Parameter Type to an existing name
    assert_cannot_rename_plugin_parameter_type_to_existing_name(
        client,
        id=plugin_param_type1["id"],
        existing_name=plugin_param_type3["name"],
        new_structure=None,
        new_description=None,
    )


def test_cannot_create_existing_plugin_parameter_type(
    client: FlaskClient,
    db: SQLAlchemy,
    auth_account: dict[str, Any],
    registered_plugin_parameter_types: dict[str, Any],
) -> None:
    """Test that creating an existing Plugin Parameter Type produces an error.

    This test validates the following sequence of actions:
    - A user attempts to create a plugin parameter type with a name that already
      exists.
    - This causes a 400 error to be returned.
    """
    existing_plugin_param_type = registered_plugin_parameter_types["plugin_param_type1"]

    assert_cannot_create_existing_plugin_parameter_type(
        client,
        name=existing_plugin_param_type,
        group_id=auth_account["groups"][0]["id"],
    )


def test_cannot_retrieve_nonexistent_plugin_parameter_type(
    client: FlaskClient, db: SQLAlchemy, auth_account: dict[str, Any]
) -> None:
    """Test that retrieving an nonexistent Plugin Parameter Type produces an error.

    This test validates the following sequence of actions:
    - A user attempts to retrieve a plugin parameter type that doesn't exist.
    - This causes a 404 error to be returned.
    """
    assert_plugin_parameter_type_is_not_found(client, id=42)
