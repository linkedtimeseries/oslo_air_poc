from datetime import datetime, timezone
from urllib.parse import urljoin, urlencode
import dateutil.parser as parser

from mapping import DataMapper

# see https://smart-data-models.github.io/dataModel.Environment/AirQualityObserved/examples/example.jsonld


def create_page_id(base_uri):
    now = datetime.now(timezone.utc)
    query = "?" + urlencode(dict(ts=now.isoformat()))
    return urljoin(urljoin(base_uri, './data'), query)


def create_observation_id(obj):
    return "urn:ngsi-ld:idlab:AirQualityObserved:{}".format(obj['id'])


def create_sensor_id(base_uri, obj):
    path = "./data/sensors/{}".format(obj['id'])
    return urljoin(base_uri, path)


def map_obs_time(obj):
    return parser.parse(obj["timestamp"]).isoformat() + "Z"


def map_location(obj):
    coords = [float(obj['latitude']), float(obj['longitude'])]
    if obj['altitude']:
        coords.append(float(obj['altitude']))
    return {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": coords
        }
    }


def map_observations(result, obj):
    for sensor_value in obj['sensordatavalues']:
        if 'id' not in sensor_value:
            continue

        raw_prop = sensor_value['value_type']

        if raw_prop == 'temperature':
            result['temperature'] = {
                "type": "Property",
                "value": float(sensor_value["value"]),
            }
        elif raw_prop == 'humidity':
            result['relativeHumidity'] = {
                "type": "Property",
                "value": float(sensor_value["value"]),
            }
        elif raw_prop == 'P1':
            result['pm10'] = {
                "type": "Property",
                "value": float(sensor_value["value"]),
                "unitCode":	"GQ",
            }
        elif raw_prop == 'P2':
            result['pm25'] = {
                "type": "Property",
                "value": float(sensor_value["value"]),
                "unitCode":	"GQ",
            }
        elif raw_prop == 'pressure':
            result['atmosphericPressure'] = {
                "type": "Property",
                "value": float(sensor_value["value"]),
                "unitCode":	"A97",
            }


def map_object(base_uri, obj):
    # todo map sensor

    result = {
        "id": create_observation_id(obj),
        "type": "AirQualityObserved",
        "dateObserved": {
            "type": "Property",
            "value": map_obs_time(obj)
        },
        "location": map_location(obj['location']),
        "@context": [
            "https://smartdatamodels.org/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }

    map_observations(result, obj)

    return result


class SDMMapper(DataMapper):
    @classmethod
    def map_data(_cls, source, base_uri, raw):
        observations = [map_object(base_uri, obj) for obj in raw]
        observations = [x for x in observations if x]

        return {
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
