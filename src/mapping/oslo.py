from datetime import datetime, timezone
from urllib.parse import urljoin, urlencode
import dateutil.parser as parser

from mapping import DataMapper

def create_page_id(base_uri):
    now = datetime.now(timezone.utc)
    query = "?" + urlencode(dict(ts=now.isoformat()))
    return urljoin(urljoin(base_uri, '/data'), query)

def create_obs_collection_id(base_uri, obj):
    path = "/data/observations/{}".format(obj['id'])
    return urljoin(base_uri, path)

def create_sensor_id(base_uri, obj):
    path = "/data/sensors/{}".format(obj['id'])
    return urljoin(base_uri, path)

def map_location(base_uri, obj):
    wkt_point = "POINT({} {} {})".format(obj['latitude'], obj['longitude'], obj['altitude'])
    return {
        "@type": "SpatialSamplingFeature",
        "SamplingFeature.sampledFeature": "http://www.wikidata.org/entity/Q56245086",
        "http://www.w3.org/ns/locn#geometry": {
            "@type": "Geometry",
            "Geometry.asWkt": "<http://www.opengis.net/def/crs/EPSG/0/4979> {}".format(wkt_point)
        },
    }

def map_sensor(base_uri, obj):
    return {
        "@type": ["Sensor", "Device"],
        "@id": create_sensor_id(base_uri, obj),
        "Device.manufacturerName": obj["sensor_type"]["manufacturer"],
        "Device.modelName": obj["sensor_type"]["name"],
    }

def map_obs_time(obj):
    return parser.parse(obj["timestamp"]).isoformat() + "Z"

def map_obs_member(base_uri, obj):
    if 'id' not in obj:
        return None

    raw_prop = obj['value_type']

    result = {
        "type": "Observation",
        "@id": create_obs_collection_id(base_uri, obj),
    }

    if raw_prop == 'temperature':
        result["Observation.observedProperty"] = "http://www.wikidata.org/entity/Q11466"
        result["Observation.hasSimpleResult"] = {
            "@type": "http://w3id.org/lindt/custom_datatypes#temperature",
            "@value": "{} Cel".format(obj["value"])
        }
    elif raw_prop == 'humidity':
        result["Observation.observedProperty"] = "http://www.wikidata.org/entity/Q2499617"
        result["Observation.hasSimpleResult"] = {
            "@type": "http://w3id.org/lindt/custom_datatypes#dimensionless",
            "@value": "{} %".format(obj["value"])
        }
    elif raw_prop == 'P1':
        result["Observation.observedProperty"] = "http://www.wikidata.org/entity/Q48035511"
        result["Observation.hasSimpleResult"] = {
            "@type": "http://w3id.org/lindt/custom_datatypes#ucum",
            "@value": "{} ug/m3".format(obj["value"])
        }
    elif raw_prop == 'P2':
        result["Observation.observedProperty"] = "http://www.wikidata.org/entity/Q48035814"
        result["Observation.hasSimpleResult"] = {
            "@type": "http://w3id.org/lindt/custom_datatypes#ucum",
            "@value": "{} ug/m3".format(obj["value"])
        }
    elif raw_prop == 'pressure':
        result["Observation.observedProperty"] = "http://www.wikidata.org/entity/Q81809"
        result["Observation.hasSimpleResult"] = {
            "@type": "http://w3id.org/lindt/custom_datatypes#pressure",
            "@value": "{} Pa".format(obj["value"])
        }
    else:
        return None
    
    return result

def map_object(base_uri, obj):
    members = [map_obs_member(base_uri, x) for x in obj['sensordatavalues']]
    members = [x for x in members if x]

    if members:
        return {
            "@id": create_obs_collection_id(base_uri, obj),
            "@type": "ObservationCollection",
            "ObservationCollection.hasFeatureOfInterest": map_location(base_uri, obj['location']),
            "ObservationCollection.madeBySensor": map_sensor(base_uri, obj['sensor']),
            "ObservationCollection.resultTime": map_obs_time(obj),
            "ObservationCollection.hasMember": members,
        }

class OsloMapper(DataMapper):
    def map_data(source, base_uri, raw):
        observations = [map_object(base_uri, obj) for obj in raw]
        observations = [x for x in observations if x]

        return {
            '@context': 'https://test.data.vlaanderen.be/doc/applicatieprofiel/AirAndWater/Core/ontwerpstandaard/2021-04-16/context/OSLO-airAndWater-Core-ap.jsonld',
            '@id': create_page_id(base_uri),
            'http://www.w3.org/ns/prov#wasGeneratedBy': {
                'http://www.w3.org/ns/prov#used': {
                    '@id': source
                },
                'http://www.w3.org/ns/prov#endedAtTime': {
                    "@type": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "@value": datetime.now(timezone.utc).isoformat(),
                }
            },
            '@included': observations
        }
