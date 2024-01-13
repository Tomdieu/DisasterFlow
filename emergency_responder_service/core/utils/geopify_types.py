from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Datasource:
    sourcename: str
    attribution: str
    license: str
    url: str

@dataclass
class Timezone:
    name: str
    name_alt: str
    offset_STD: str
    offset_STD_seconds: int
    offset_DST: str
    offset_DST_seconds: int
    abbreviation_STD: str
    abbreviation_DST: str

@dataclass
class Bbox:
    lon1: float
    lat1: float
    lon2: float
    lat2: float

@dataclass
class Rank:
    importance: float
    popularity: float
    confidence: int
    confidence_city_level: int
    confidence_street_level: int
    match_type: str

@dataclass
class Query:
    text: str
    parsed: dict

@dataclass
class GeoapifyResult:
    datasource: Datasource
    name: str
    country: str
    country_code: str
    state: str
    county: str
    city: str
    district: str
    suburb: str
    street: str
    lon: float
    lat: float
    state_code: str
    formatted: str
    address_line1: str
    address_line2: str
    category: str
    timezone: Timezone
    plus_code: str
    plus_code_short: str
    result_type: str
    rank: Rank
    place_id: str
    bbox: Bbox

@dataclass
class GeoapifyResponse:
    results: List[GeoapifyResult]
    query: Query


from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Location:
    lat: float
    lon: float

@dataclass
class Instruction:
    from_index: int
    to_index: int
    distance: int
    time: float
    instruction_text: str

@dataclass
class Step:
    from_index: int
    to_index: int
    distance: int
    time: float
    instruction: Instruction

@dataclass
class Leg:
    distance: int
    time: float
    steps: List[Step]

@dataclass
class Geometry:
    type: str
    coordinates: List[List[List[float]]]

@dataclass
class FeatureProperties:
    mode: str
    waypoints: List[Location]
    units: str
    distance: int
    distance_units: str
    time: float
    legs: List[Leg]

@dataclass
class Feature:
    type: str
    properties: FeatureProperties
    geometry: Geometry

@dataclass
class RoutingResponse:
    features: List[Feature]
    properties: dict
    type: str
