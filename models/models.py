from pydantic import BaseModel
from datetime import datetime

class Location(BaseModel):
    lat: float
    lng: float

class TruckLocation(BaseModel):
    vehicle_id: str
    timestamp: datetime
    location: Location
    status: dict

class Truck(BaseModel):
    vehicle_id: str
    description: dict

class Route(BaseModel):
    location_start: Location
    location_end: Location
    datetime_start: datetime
    datetime_end: datetime

class TruckRoute(BaseModel):
    truck: Truck
    route: Route
