# OSLO Air proof of concept

## Install

```
git clone git@github.com:linkedtimeseries/oslo_air_poc.git
cd oslo_air_poc
python src/app.py
```

Open `http://localhost:5000/oslo` to see Luftdaten observations published with [LDES](https://w3id.org/ldes/specification) and described with the OSLO Application Profile [Air Quality](https://purl.eu/doc/applicationprofile/AirAndWater/Air/)

Open `http://localhost:5000/smart_data_models` for Luftdaten observations using normalized [Smart Data Models](https://smartdatamodels.org/), and 
 `http://localhost:5000/smart_data_models_kv` for its `keyValues` representation.

Open `http://localhost:5000/json_ld_star` for Luftdaten observations using the [property graph model RDF*](https://json-ld.github.io/json-ld-star/) in JSON-LD format.

## Configure

Adapt the `src/config.toml` file:
- the Luftdaten API to fetch, for example by changing the country code in the query parameter.
- the polling interval
- the base URI for the generated identifiers

## Docker

A Docker file is provided:

```
docker build -t server .
docker run -p 5000:80 server
```

Or use the docker-compose file:
```
docker build -t server .
docker-compose up
```