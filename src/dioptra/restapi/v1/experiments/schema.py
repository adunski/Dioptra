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
"""The schemas for serializing/deserializing Experiment resources."""
from __future__ import annotations

from marshmallow import Schema, fields

from dioptra.restapi.v1.schemas import (
    BasePageSchema,
    GroupIdQueryParametersSchema,
    PagingQueryParametersSchema,
    SearchQueryParametersSchema,
    generate_base_resource_ref_schema,
    generate_base_resource_schema,
)

ExperimentRefBaseSchema = generate_base_resource_ref_schema("Experiment")


class ExperimentRefSchema(ExperimentRefBaseSchema):  # type: ignore
    """The reference schema for the data stored in a Experiment resource."""

    name = fields.String(
        attribute="name",
        metadata=dict(description="Name of the Experiment resource."),
    )


class ExperimentMutableFieldsSchema(Schema):
    """The fields schema for the mutable data in a Experiment resource."""

    name = fields.String(
        attribute="name", metadata=dict(description="Name of the Experiment resource.")
    )


ExperimentBaseSchema = generate_base_resource_schema("Experiment", snapshot=True)


class ExperimentSchema(ExperimentMutableFieldsSchema, ExperimentBaseSchema):  # type: ignore
    """The schema for the data stored in a Experiment resource."""


class ExperimentPageSchema(BasePageSchema):
    """The paged schema for the data stored in a Experiment resource."""

    data = fields.Nested(
        ExperimentSchema,
        many=True,
        metadata=dict(description="List of Experiment resources in the current page."),
    )


class ExperimentGetQueryParameters(
    PagingQueryParametersSchema,
    GroupIdQueryParametersSchema,
    SearchQueryParametersSchema,
):
    """The query parameters for the GET method of the /Experiments endpoint."""
