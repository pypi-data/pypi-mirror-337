from datetime import datetime
from typing import Optional

from pydantic.dataclasses import dataclass

from kumoapi.common import StrEnum
from kumoapi.data_snapshot import GraphSnapshotID


@dataclass
class OnlinePredictionOptions:
    # Required if prediction task is to perform binary classification.
    binary_classification_threshold: Optional[float] = None

    # On classification tasks, for each entity, we will only return predictions
    # for the K classes with the highest predicted values for the entity.
    # If empty, predict all class. This field is ignored for regression tasks.
    num_classes_to_return: Optional[int] = None


# Request body for either launch or patch(update) an online serving endpoint:
#
# To launch one:
#    POST /online_serving_endpoints {OnlineServingEndpointRequest body}
#      => return {OnlineServingEndpointResource} + 200 (upon success)
# To update one:
#    PATCH /online_serving_endpoints/{id} {OnlineServingEndpointRequest body}
#      => return {OnlineServingEndpointResource} + 200 (upon success)
@dataclass
class OnlineServingEndpointRequest:
    """POST request body to create an Online Serving endpoint."""
    # ID of a (successful) model training job.
    model_training_job_id: str

    predict_options: OnlinePredictionOptions

    # Optional, a specific Graph data snapshot to be loaded for online
    # prediction. If this field is absent in the launch or update request,
    # this instructs Kumo to refresh the graph data and load the most
    # recently refreshed graph data snapshot for online serving.
    graph_snapshot_id: Optional[GraphSnapshotID] = None

    # Estimated max # of requests per second. This field can be useful for Kumo
    # to provision sufficient serving capacity and to configure rate limiting
    # and/or load shedding.
    max_qps: int = 50


class OnlineServingStatusCode(StrEnum):
    # Online serving endpoint is alive and ready to accept traffic
    READY = 'ready'
    # We are still in progress to materialize data, provision resources,
    # or starting up server replicas.
    IN_PROGRESS = 'in_progress'

    # Failed to launch online serving endpoint, likely due to reasons such as
    # using an old model incompatible with online serving, insufficient
    # resources to launch too many replicas, etc.
    FAILED = 'failed'


@dataclass
class OnlineServingStatus:
    status_code: OnlineServingStatusCode

    # Most recently updated timestamp of current status.
    last_updated_at: datetime

    # Current stage while status_code is IN_PROGRESS.
    stage: Optional[str] = None
    # Message if status_code is FAILED.
    failure_message: Optional[str] = None


@dataclass
class OnlineServingUpdate:
    """
    Information/status about an update (PATCH) operation on an existing
    online serving endpoint.
    """
    prev_config: OnlineServingEndpointRequest
    target_config: OnlineServingEndpointRequest

    update_started_at: datetime
    update_status: OnlineServingStatus


@dataclass
class OnlineServingEndpointResource:
    id: str

    # Endpoint url would formatted as "<kumo cloud hostname>/gira/{id}"
    # where <kumo cloud hostname> is typical the your Kumo cloud web url such
    # as "https://<customer_id>.kumoai.cloud"
    endpoint_url: str

    config: OnlineServingEndpointRequest

    # Timestamp of when this endpoint resoruce was create.
    launched_at: datetime

    # Current status. The endpoint_url will be ready to serve traffic only if
    # status.status_code is READY
    status: OnlineServingStatus

    # The info/status about the most recent UPDATE operation on this endpoint,
    # if any.  Note that if the last update status is READY,
    # `update.target_config` would be identical to the `config` field,
    # otherwise `update.prev_config` would be identical to the `config` field.
    update: Optional[OnlineServingUpdate] = None
