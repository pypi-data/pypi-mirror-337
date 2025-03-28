from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ServiceType(str, Enum):
    dap = "dap2"
    edr = "edr"
    wms = "wms"
    zarr = "zarr"


class ServiceStatus(str, Enum):
    available = "available"
    progressing = "progressing"
    unknown = "unknown"
    error = "error"


class ServiceConfig(BaseModel):
    service_type: ServiceType
    org: str

    # NOTE: This is necessary to have our unauthenticated, public-facing demos.
    #
    # NOTE: An org can only have one public or private instance of a given
    # service deployed at a time, as the routing is ambiguous if we were to
    # support multiple different instances.
    is_public: bool

    # Optional Booth image tag
    service_version: Optional[str] = None

    # Optional number of replicas
    replicas: Optional[int] = 1

    # Optional Booth dataset cache duration (in seconds)
    dataset_cache_ttl: Optional[int] = 60

    # Optional Booth dataset cache max number of datasets
    dataset_cache_size: Optional[int] = 10

    # Optional cache max-age for cache control headers of the service responses (in seconds)
    # If not set, the default is 0, which means functionally no caching, but requests are revalidated.
    cache_max_age: Optional[int] = 0

    # Optional zarr concurrency configuration, the number of concurrent reads zarr will use fulfilling requests
    zarr_concurrency: Optional[int] = 10

    def __str__(self) -> str:
        return f"{self.service_type.name}://{self.org}"


class DeploymentInfo(BaseModel):
    """Compute deployment information."""

    name: str
    url: str
    created: datetime
    config: ServiceConfig
    status: ServiceStatus


class LoadResults(BaseModel):
    succeeded: list[str]
    failed: list[str]


class ComputeConfig(BaseModel):
    service_uri: str
    domain: str
    env: str
    container_repository: str
    kube_config: dict
    openmeter_api_key: Optional[str] = None


class LogMessage(BaseModel):
    time: str
    message: str

    def __str__(self) -> str:
        return f"{self.time} | {self.message}\n"
