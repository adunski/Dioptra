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
"""The schemas for serializing/deserializing Plugin resources."""
from __future__ import annotations

from marshmallow import Schema, fields

from dioptra.restapi.v1.groups.schema import GroupRefSchema
from dioptra.restapi.v1.schemas import (
    generate_base_resource_schema,
    BasePageSchema,
    GroupIdQueryParametersSchema,
    PagingQueryParametersSchema,
    SearchQueryParametersSchema,
)
from dioptra.restapi.v1.tags.schema import TagRefSchema
from dioptra.restapi.v1.users.schema import UserRefSchema
from dioptra.restapi.v1.plugin_parameter_types.schema import (
    PluginParameterTypeRefSchema,
)


class PluginRefSchema(Schema):
    """The reference schema for the data stored in a Plugin resource."""

    id = fields.Integer(
        attribute="id",
        metadata=dict(description="ID for the Plugin resource."),
    )
    group = fields.Nested(
        GroupRefSchema,
        attribute="group",
        metadata=dict(description="Group that owns the Plugin resource."),
    )
    name = fields.String(
        attribute="name",
        metadata=dict(description="Name of the Plugin resource."),
    )
    url = fields.Url(
        attribute="url",
        metadata=dict(description="URL for accessing the full Plugin resource."),
        relative=True,
    )


class PluginFileRefSchema(Schema):
    """The reference schema for the data stored in a PluginFile."""

    id = fields.Integer(
        attribute="id",
        metadata=dict(description="ID for the PluginFile resource."),
    )
    plugin_id = fields.Int(
        attribute="plugin_id",
        metadata=dict(description="ID for the Plugin resource this file belongs to."),
    )
    filename = fields.String(
        attribute="filename",
        metadata=dict(description="Filename of the PluginFile resource."),
    )
    url = fields.Url(
        attribute="url",
        metadata=dict(description="URL for accessing the full PluginFile resource."),
        relative=True,
    )


class PluginTaskSchema(Schema):
    """The schema for the data stored in a PluginTask."""

    name = fields.String(
        attribute="name",
        metadata=dict(description="Name of the PluginTask."),
    )

    number = fields.Integer(
        attribute="number",
        metadata=dict(description="The positional order of the parameter."),
    )

    input_params = fields.Nested(
        PluginParameterTypeRefSchema,
        many=True,
        metadata=dict(
            description="List of input PluginTaskParameters in this PluginTask."
        ),
    )

    output_params = fields.Nested(
        PluginParameterTypeRefSchema,
        many=True,
        metadata=dict(
            description="List of output PluginTaskParameters in this PluginTask."
        ),
    )


class PluginMutableFieldsSchema(Schema):
    """The schema for the mutable data fields in a Plugin resource."""

    name = fields.String(
        attribute="name", metadata=dict(description="Name of the Plugin resource.")
    )


PluginBaseSchema = generate_base_resource_schema("Plugin")


class PluginSchema(PluginMutableFieldsSchema, PluginBaseSchema):
    """The schema for the data stored in a Plugin resource."""

    files = fields.Nested(
        PluginFileRefSchema,
        attribute="files",
        metadata=dict(description="Files associated with the Plugin resource."),
        many=True,
        dump_only=True,
    )


class PluginPageSchema(BasePageSchema):
    """The paged schema for the data stored in a Plugin resource."""

    data = fields.Nested(
        PluginSchema,
        many=True,
        metadata=dict(description="List of Plugin resources in the current page."),
    )


class PluginGetQueryParameters(
    PagingQueryParametersSchema,
    GroupIdQueryParametersSchema,
    SearchQueryParametersSchema,
):
    """The query parameters for the GET method of the /queues endpoint."""


class PluginFileMutableFieldsSchema(Schema):
    """The schema for the mutable data fields in a PluginFile resource."""

    filename = fields.String(
        attribute="name", metadata=dict(description="Name of the PluginFile resource.")
    )

    contents = fields.String(
        attribute="contents", metadata=dict(description="Contents of the file.")
    )


PluginFileBaseSchema = generate_base_resource_schema("PluginFile")


class PluginFileSchema(PluginFileMutableFieldsSchema, PluginFileBaseSchema):
    """The schema for the data stored in a PluginFile resource."""

    tasks = fields.Nested(
        PluginTaskSchema,
        attribute="tasks",
        metadata=dict(description="Tasks associated with the PluginFile resource."),
        many=True,
        dump_only=True,
    )


class PluginFilePageSchema(BasePageSchema):
    """The paged schema for the data stored in a PluginFile resource."""

    data = fields.Nested(
        PluginFileSchema,
        many=True,
        metadata=dict(description="List of PluginFile resources in the current page."),
    )


class PluginFileGetQueryParameters(
    PagingQueryParametersSchema,
):
    """The query parameters for the GET method of the /queues/{id}/files/ endpoint."""
