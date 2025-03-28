from decimal import Decimal

import orjson
from pydantic import BaseModel, Field

from iikocloudapi.client import Client
from iikocloudapi.helpers import BaseResponseModel


class CouriersLocationsByTimeOffset(BaseResponseModel):
    class CourierLocation(BaseModel):
        class Item(BaseModel):
            class Location(BaseModel):
                latitude: Decimal
                longitude: Decimal
                server_timestamp: int = Field(alias="serverTimestamp")

            courier_id: str = Field(alias="courierId")
            locations: list[Location]

        organization_id: str = Field(alias="organizationId")
        items: list[Item]

    courier_locations: list[CourierLocation] = Field(alias="courierLocations")


class Employees:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def couriers_locations_by_time_offset(
        self,
        organization_ids: str,
        offset_in_seconds: int | None = None,
        timeout: str | int | None = None,
    ) -> CouriersLocationsByTimeOffset:
        response = await self._client.request(
            "/api/1/employees/couriers/locations/by_time_offset",
            data={
                "organizationIds": organization_ids,
                "offsetInSeconds": offset_in_seconds,
            },
            timeout=timeout,
        )
        return CouriersLocationsByTimeOffset(**orjson.loads(response.content))
