import requests

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Dict


app = FastAPI()


class Station(BaseModel):
    id: str
    name: str
    address: str
    capacity: int
    available_bikes: int | None
    available_docks: int | None

    def update(self, data: Dict):
        for key, value in data.items():
            setattr(self, key, value)
        return self


class StationResponse(BaseModel):
    success: bool
    data: list[Station]


@app.get("/stations", response_model=StationResponse)
async def get_stations(
    available_bike_filter: bool = Query(default=False, description="Filter on has available bikes."),
    available_dock_filter: bool = Query(default=False, description="Filter on has an available dock."),
):
    # Two sources of data to be merged.
    raw_station_info_json = requests.get('https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json').json()
    raw_station_status_json = requests.get('https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json').json()

    stations = {} # dict as {id: Station}

    for row in raw_station_info_json['data']['stations']:
        id = row.get('station_id')
        stations[id] = Station(
            id = id,
            name = row.get('name'),
            address = row.get('address'),
            capacity = row.get('capacity'),
        )
        
    for row in raw_station_status_json['data']['stations']:
        id = row.get('station_id')
        stations[id].update({
            'available_bikes': row.get('num_bikes_available'),
            'available_docks': row.get('num_docks_available'),
        })

    result = []
    for station in stations.values():
        if available_bike_filter and station.available_bikes == 0:
            continue
        if available_dock_filter and station.available_docks == 0:
            continue

        result.append(station)

    return StationResponse(success=True, data=result)
