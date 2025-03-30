import os
from typing import Any

from crudclient.client import Client

from .config import TripletexConfig, TripletexTestConfig


class TripletexClient(Client):
    def __init__(self, config: TripletexConfig | None = None) -> None:
        if config is None:
            config = TripletexTestConfig() if os.getenv("DEBUG", "") == "1" else TripletexConfig()

        super().__init__(config=config)

    def _request(self, method: str, endpoint: str | None = None, url: str | None = None, **kwargs) -> Any:
        return super()._request(method, endpoint, url, handle_response=method != "DELETE", **kwargs)
