from datetime import datetime, timezone
from urllib.parse import urljoin, urlencode
import dateutil.parser as parser

from mapping import DataMapper


def create_page_id(base_uri):
    now = datetime.now(timezone.utc)
    query = "?" + urlencode(dict(ts=now.isoformat()))
    return urljoin(urljoin(base_uri, './data'), query)


def create_obs_collection_id(base_uri, obj):
    path = "./data/observations/{}".format(obj['id'])
    return urljoin(base_uri, path)


def create_sensor_id(base_uri, obj):
    path = "./data/sensors/{}".format(obj['id'])
    return urljoin(base_uri, path)

def create_ldes_id(base_uri):
    return urljoin(urljoin(base_uri, './oslo'), '#feed')

def create_shacl_id(base_uri, node):
    return urljoin(urljoin(base_uri, '#shape'), node)

def create_shacl(base_uri):
    return {
        '@type': 'http://www.w3.org/ns/shacl#NodeShape',
        'http://www.w3.org/ns/shacl#sh:targetClass': {
            '@id': 'ObservationCollection'
        },
        'http://www.w3.org/ns/shacl#property': [
            {
                'http://www.w3.org/ns/shacl#path': 'http://www.w3.org/ns/sosa/resultTime',
                'http://www.w3.org/ns/shacl#datatype': 'http://www.w3.org/2001/XMLSchema#dateTime',
                'http://www.w3.org/ns/shacl#maxCount': 1
            },
            {
                'http://www.w3.org/ns/shacl#path': 'http://www.w3.org/ns/sosa/madeBySensor',
                'http://www.w3.org/ns/shacl#class': 'http://www.w3.org/ns/sosa/Sensor',
                'http://www.w3.org/ns/shacl#nodeKind': 'http://www.w3.org/ns/shacl#IRI',
                'http://www.w3.org/ns/shacl#maxCount': 1,
                'http://www.w3.org/ns/shacl#node': {
                    '@type': 'http://www.w3.org/ns/shacl#NodeShape',
                    'http://www.w3.org/ns/shacl#sh:targetClass': [{
                        '@id': 'Sensor'
                    }, {
                        '@id': 'Device'
                    }],
                    'http://www.w3.org/ns/shacl#property': [{
                        'http://www.w3.org/ns/shacl#path': 'Device.manufacturerName',
                        'http://www.w3.org/ns/shacl#nodeKind': 'http://www.w3.org/2000/01/rdf-schema#Literal',
                        'http://www.w3.org/ns/shacl#minCount': 1,
                        'http://www.w3.org/ns/shacl#maxCount': 1
                    }, {
                        'http://www.w3.org/ns/shacl#path': 'Device.modelName',
                        'http://www.w3.org/ns/shacl#nodeKind': 'http://www.w3.org/2000/01/rdf-schema#Literal',
                        'http://www.w3.org/ns/shacl#minCount': 1,
                        'http://www.w3.org/ns/shacl#maxCount': 1
                    }]
                }
            },
            {
                'http://www.w3.org/ns/shacl#path': 'http://www.w3.org/ns/sosa/hasMember',
                'http://www.w3.org/ns/shacl#class': 'http://def.isotc211.org/iso19156/2011/Observation#OM_Observation',
                'http://www.w3.org/ns/shacl#nodeKind': 'http://www.w3.org/ns/shacl#IRI',
                'http://www.w3.org/ns/shacl#minCount': 1,
                'http://www.w3.org/ns/shacl#node': {
                    '@type': 'http://www.w3.org/ns/shacl#NodeShape',
                    'http://www.w3.org/ns/shacl#sh:targetClass': {
                        '@id': 'http://def.isotc211.org/iso19156/2011/Observation#OM_Observation'
                    },
                    'http://www.w3.org/ns/shacl#property': [{
                        'http://www.w3.org/ns/shacl#path': 'Observation.observedProperty',
                        'http://www.w3.org/ns/shacl#nodeKind': 'http://www.w3.org/ns/shacl#IRI',
                        'http://www.w3.org/ns/shacl#minCount': 1,
                        'http://www.w3.org/ns/shacl#maxCount': 1
                    }, {
                        'http://www.w3.org/ns/shacl#path': 'Observation.hasSimpleResult',
                        'http://www.w3.org/ns/shacl#nodeKind': 'http://www.w3.org/2000/01/rdf-schema#Literal',
                        'http://www.w3.org/ns/shacl#minCount': 1,
                        'http://www.w3.org/ns/shacl#maxCount': 1
                    }]
                }
            },
            {
                'http://www.w3.org/ns/shacl#path': 'http://www.w3.org/ns/sosa/hasFeatureOfInterest',
                'http://www.w3.org/ns/shacl#class': 'https://def.isotc211.org/iso19156/2011/GeneralFeatureInstance#GFI_Feature',
                'http://www.w3.org/ns/shacl#nodeKind': 'http://www.w3.org/ns/shacl#IRI',
                'http://www.w3.org/ns/shacl#maxCount': 1,
                'http://www.w3.org/ns/shacl#node': {
                    '@type': 'http://www.w3.org/ns/shacl#NodeShape',
                    'http://www.w3.org/ns/shacl#sh:targetClass': {
                        '@id': 'SpatialSamplingFeature'
                    },
                    'http://www.w3.org/ns/shacl#property': [{
                        'http://www.w3.org/ns/shacl#path': 'SamplingFeature.sampledFeature',
                        'http://www.w3.org/ns/shacl#nodeKind': 'http://www.w3.org/ns/shacl#IRI',
                        'http://www.w3.org/ns/shacl#minCount': 1,
                        'http://www.w3.org/ns/shacl#maxCount': 1
                    }, {
                        'http://www.w3.org/ns/shacl#path': 'http://www.w3.org/ns/locn#geometry',
                        'http://www.w3.org/ns/shacl#nodeKind': 'http://www.w3.org/ns/shacl#IRI',
                        'http://www.w3.org/ns/shacl#minCount': 1,
                        'http://www.w3.org/ns/shacl#maxCount': 1,
                        'http://www.w3.org/ns/shacl#node': {
                            '@type': 'http://www.w3.org/ns/shacl#NodeShape',
                            'http://www.w3.org/ns/shacl#sh:targetClass': {
                                '@id': 'Geometry'
                            },
                            'http://www.w3.org/ns/shacl#property': [{
                                'http://www.w3.org/ns/shacl#path': 'Geometry.asWkt',
                                'http://www.w3.org/ns/shacl#nodeKind': 'http://www.w3.org/2000/01/rdf-schema#Literal',
                                'http://www.w3.org/ns/shacl#minCount': 1,
                                'http://www.w3.org/ns/shacl#maxCount': 1
                            }]
                        }
                    }]
                }
            }
        ]
    }



def map_location(base_uri, obj):
    wkt_point = "POINT({} {} {})".format(
        obj['latitude'], obj['longitude'], obj['altitude'])
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
            "@reverse": {
                "tree:member": create_ldes_id(base_uri)
            }
        }

class OsloMapper(DataMapper):
    @classmethod
    def map_data(_cls, source, base_uri, raw):
        observations = [map_object(base_uri, obj) for obj in raw]
        observations = [x for x in observations if x]

        return {
            '@context': ['https://brechtvdv.github.io/demo-data/OSLO-airAndWater-Core-ap.jsonld', {
                'ldes': 'https://w3id.org/ldes#',
                'tree': 'https://w3id.org/tree#',
                'tree:member': {
                    '@type': '@id'
                }
            }],
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
            '@reverse': {
                'tree:view': {
                    '@id': create_ldes_id(base_uri),
                    '@type': 'ldes:EventStream',
                    'ldes:timestampPath': 'ObservationCollection.resultTime',
                    'tree:shape': create_shacl(base_uri)
                }
            },
            '@included': observations
        }
