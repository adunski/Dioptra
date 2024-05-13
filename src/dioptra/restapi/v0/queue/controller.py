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
"""The module defining the queue endpoints."""
from __future__ import annotations

import uuid
from typing import Any, cast

import structlog
from flask import request
from flask_accepts import accepts, responds
from flask_login import login_required
from flask_restx import Namespace, Resource
from injector import inject
from structlog.stdlib import BoundLogger

from dioptra.restapi.db.legacy_models import LegacyQueue

from .schema import IdStatusResponseSchema, NameStatusResponseSchema, QueueSchema
from .service import QueueNameService, QueueService

LOGGER: BoundLogger = structlog.stdlib.get_logger()

api: Namespace = Namespace(
    "Queue",
    description="Queue registration operations",
)


@api.route("/")
class QueueResource(Resource):
    """Shows a list of all queues, and lets you POST to register new ones."""

    @inject
    def __init__(self, *args, queue_service: QueueService, **kwargs) -> None:
        self._queue_service = queue_service
        super().__init__(*args, **kwargs)

    @login_required
    @responds(schema=QueueSchema(many=True), api=api)
    def get(self) -> list[LegacyQueue]:
        """Gets a list of all active queues."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="queue", request_type="GET"
        )  # noqa: F841
        log.info("Request received")
        return self._queue_service.get_all_unlocked(log=log)

    @login_required
    @accepts(schema=QueueSchema, api=api)
    @responds(schema=QueueSchema, api=api)
    def post(self) -> LegacyQueue:
        """Registers a new queue.

        Note that the name of the queue will be slugified and must remain unique after \
        slugification. For example, the name "My Queue" would be slugified to \
        "my-queue".
        """
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="queue", request_type="POST"
        )  # noqa: F841
        log.info("Request received")
        parsed_obj = request.parsed_obj  # type: ignore
        return self._queue_service.create(name=parsed_obj["name"], log=log)


@api.route("/<int:queueId>")
@api.param("queueId", "An integer identifying a registered queue.")
class QueueIdResource(Resource):
    """Shows a single queue (id reference) and lets you modify and delete it."""

    @inject
    def __init__(self, *args, queue_service: QueueService, **kwargs) -> None:
        self._queue_service = queue_service
        super().__init__(*args, **kwargs)

    @login_required
    @responds(schema=QueueSchema, api=api)
    def get(self, queueId: int) -> LegacyQueue:
        """Gets a queue by its unique identifier."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="queueId", request_type="GET"
        )  # noqa: F841
        log.info("Request received", queue_id=queueId)
        return cast(
            LegacyQueue,
            self._queue_service.get(queueId, error_if_not_found=True, log=log),
        )

    @login_required
    @responds(schema=IdStatusResponseSchema, api=api)
    def delete(self, queueId: int) -> dict[str, Any]:
        """Deletes a queue by its unique identifier."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="queueId", request_type="DELETE"
        )  # noqa: F841
        log.info("Request received", queue_id=queueId)
        return self._queue_service.delete(queueId, log=log)

    @login_required
    @accepts(schema=QueueSchema, api=api)
    @responds(schema=QueueSchema, api=api)
    def put(self, queueId: int) -> LegacyQueue:
        """Modifies a queue by its unique identifier."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="queueId", request_type="PUT"
        )  # noqa: F841
        parsed_obj = request.parsed_obj  # type: ignore
        return self._queue_service.rename(queueId, new_name=parsed_obj["name"], log=log)


@api.route("/<int:queueId>/lock")
@api.param("queueId", "An integer identifying a registered queue.")
class QueueIdLockResource(Resource):
    """Lets you put a lock on a queue (id reference) and lets you delete it."""

    @inject
    def __init__(self, *args, queue_service: QueueService, **kwargs) -> None:
        self._queue_service = queue_service
        super().__init__(*args, **kwargs)

    @login_required
    @responds(schema=IdStatusResponseSchema, api=api)
    def delete(self, queueId: int) -> dict[str, Any]:
        """Removes the lock from the queue (id reference) if it exists."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="QueueIdLock", request_type="DELETE"
        )  # noqa: F841
        log.info("Request received", queue_id=queueId)
        return self._queue_service.unlock(queueId, log=log)

    @login_required
    @responds(schema=IdStatusResponseSchema, api=api)
    def put(self, queueId: int) -> dict[str, Any]:
        """Locks the queue (id reference) if it is unlocked."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="QueueIdLock", request_type="PUT"
        )  # noqa: F841
        log.info("Request received", queue_id=queueId)
        return self._queue_service.lock(queueId, log=log)


@api.route("/name/<string:queueName>")
@api.param("queueName", "The name of the queue.")
class QueueNameResource(Resource):
    """Shows a single queue (name reference) and lets you modify and delete it."""

    @inject
    def __init__(self, *args, queue_name_service: QueueNameService, **kwargs) -> None:
        self._queue_name_service = queue_name_service
        super().__init__(*args, **kwargs)

    @login_required
    @responds(schema=QueueSchema, api=api)
    def get(self, queueName: str) -> LegacyQueue:
        """Gets a queue by its unique name."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="queueName", request_type="GET"
        )  # noqa: F841
        log.info("Request received", queue_name=queueName)
        return cast(
            LegacyQueue,
            self._queue_name_service.get(queueName, error_if_not_found=True, log=log),
        )

    @login_required
    @responds(schema=NameStatusResponseSchema, api=api)
    def delete(self, queueName: str) -> dict[str, Any]:
        """Deletes a queue by its unique name."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()),
            resource="queueName",
            queue_name=queueName,
            request_type="DELETE",
        )  # noqa: F841
        log.info("Request received", queue_name=queueName)
        return self._queue_name_service.delete(queueName, log=log)


@api.route("/name/<string:queueName>/lock")
@api.param("queueName", "The name of the queue.")
class QueueNameLockResource(Resource):
    """Lets you put a lock on a queue (name reference) and lets you delete it."""

    @inject
    def __init__(self, *args, queue_name_service: QueueNameService, **kwargs) -> None:
        self._queue_name_service = queue_name_service
        super().__init__(*args, **kwargs)

    @login_required
    @responds(schema=NameStatusResponseSchema, api=api)
    def delete(self, queueName: str) -> dict[str, Any]:
        """Removes the lock from the queue (name reference) if it exists."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()),
            resource="QueueNameLock",
            request_type="DELETE",
        )  # noqa: F841
        log.info("Request received", queue_name=queueName)
        return self._queue_name_service.unlock(queueName, log=log)

    @login_required
    @responds(schema=NameStatusResponseSchema, api=api)
    def put(self, queueName: str) -> dict[str, Any]:
        """Locks the queue (name reference) if it is unlocked."""
        log: BoundLogger = LOGGER.new(
            request_id=str(uuid.uuid4()), resource="QueueNameLock", request_type="PUT"
        )  # noqa: F841
        log.info("Request received", queue_name=queueName)
        return self._queue_name_service.lock(queueName, log=log)
