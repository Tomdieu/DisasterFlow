from dataclasses import dataclass
from typing import List,Tuple

@dataclass
class Geometry:
    type: str
    coordinates: List[float]

@dataclass
class Point:
    type: str = "Point"
    coordinates: Tuple[float, float]

@dataclass
class Properties:
    address: str
    country: str
    city: str
    state: str  

@dataclass
class Feature:
    id: int
    type: str
    geometry: Point
    properties: Properties

@dataclass
class FeatureCollection:
    type: str
    features: List[Feature]