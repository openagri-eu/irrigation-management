# Irrigation service

# Description

The Irrigation service provides information via It's APIs, either in the form of \
ETo (Reference evapotranspiration) calculations or soil moisture analysis.

# Requirements

<ul>
    <li>git</li>
    <li>docker</li>
    <li>docker-compose</li>
</ul>

Docker version used during development: 27.0.3

# Installation

There are two ways to install this service, via docker (preferred) or directly from source.

<h3> Deploying from source </h3>

When deploying from source, use python 3:11.\
Also, you should use a [venv](https://peps.python.org/pep-0405/) when doing this.

A list of libraries that are required for this service is present in the "requirements.txt" file.\
This service uses FastAPI as a web framework to serve APIs, alembic for database migrations and sqlalchemy for database ORM mapping.

<h3> Deploying via docker </h3>

After installing <code>docker-compose</code> you can run the following commands to run the application:

```
docker compose build
docker compose up
```

The application will be served on http://127.0.0.1:80 (I.E. typing localhost/docs in your browser will load the swagger documentation)

# Documentation

Examples:

<h3>GET/DELETE</h3>

```
/api/v1/dataset/{dataset_id}
```

Example responses for GET and DELETE respectively:

```json
[
  {
    "dataset_id": 23,
    "date": "2024-10-17T13:18:05.054Z",
    "soil_moisture_10": 7.3,
    "soil_moisture_20": 2.4,
    "soil_moisture_30": 2.2,
    "soil_moisture_40": 1.3,
    "soil_moisture_50": 1.1,
    "soil_moisture_60": 1.1,
    "rain": 0.6,
    "temperature": 22.3,
    "humidity": 66.33
  }
]
```

```json
{
  "status_code":201, 
  "detail": "Successfully deleted"
}
```

<h3>POST</h3>

```
/api/v1/dataset/
```

Input JSON:

```json
{
   "dataset_id": 23,
   "date": "2024-10-17T13:18:05.054Z",
   "soil_moisture_10": 7.3,
   "soil_moisture_20": 2.4,
   "soil_moisture_30": 2.2,
   "soil_moisture_40": 1.3,
   "soil_moisture_50": 1.1,
   "soil_moisture_60": 1.1,
   "rain": 0.6,
   "temperature": 22.3,
   "humidity": 66.33
}

```

```
/api/v1/dataset/
```

Example response:
```json
{
  "dataset_id": 23,
  "date": "2024-10-17T13:18:05.054Z",
  "soil_moisture_10": 7.3,
  "soil_moisture_20": 2.4,
  "soil_moisture_30": 2.2,
  "soil_moisture_40": 1.3,
  "soil_moisture_50": 1.1,
  "soil_moisture_60": 1.1,
  "rain": 0.6,
  "temperature": 22.3,
  "humidity": 66.33 
}
```

<h3>GET</h3>

```
/api/v1/dataset/{dataset_id}/analysis
```

Example response:
```json
{
  "dataset_id": 23,
  "time_period": [
    "2024-10-17T13:24:35.198Z", "2024-10-18T13:24:35.198Z"
  ],
  "irrigation_events_detected": 12,
  "precipitation_events": 10,
  "high_dose_irrigation_events": 3,
  "high_dose_irrigation_events_dates": [
    "2024-10-17T13:24:35.198Z"
  ],
  "field_capacity": [
    [
      10,
      0.17
    ]
  ],
  "stress_level": [
    [
      10,
      0.04
    ]
  ],
  "number_of_saturation_days": 1,
  "saturation_dates": [
    "2024-10-17T13:24:35.198Z"
  ],
  "no_of_stress_days": 1,
  "stress_dates": [
    "2024-10-17T13:24:35.198Z"
  ]
}
```

<h3>GET</h3>
```
/api/v1/location/{location_id}
```

Example response:

```
{
    "id": 1,
    "city_name": "Paris",
    "state_code": none,
    "country_code": "FR"
}
```
If a state from the USA was added:
```
{
    "id": 1,
    "city_name": "Paris",
    "state_code": Texas,
    "country_code": "USA"
}
```


<h3>POST</h3>
```
/api/v1/location/
```

Example response: Same as above

<h3>DELETE</h3>
```
/api/v1/location/{location_id}
```

Example response: Same as above

<h3>POST</h3>
```
/api/v1/eto/get-calculations/{location_id}
```

Example response: 

```
{
    "calculations": [
        {
            "date": "2020-10-25",
            "value": 6.55
        },
        {
            "date": "2020-10-24",
            "value": 6.45
        },
        {
            "date": "2020-10-23",
            "value": 6.52
        },
        {
            "date": "2020-10-22",
            "value": 5.87
        }
    ]
}
```
Values represent the calculated ETo values, which are represented in mm/day or millimetres per day

<h3>Example usage for the ETo:</h3>

A user would input the location of their parcel/plot of land via the POST /api/v1/location/ API (or multiple parcels). \
The system requests weather data for these locations at around midnight every day. \
Once a user wishes to view ETo values, they may call the POST /api/v1/eto/get-calculations/{location_id} API. \
This API will return a list of calculations, for the given days.

Currently, because the service only starts collecting data once it has been deployed, it is not possible to \
query for ETo values for days before it has been deployed. 

<h3>Example usage for the soil moisture analysis:</h3>

Use POST /api/v1/dataset/ to upload your data to the database.
GET and DELETE requests with the same URL as previously mentioned are for fetching and deleting data from database, respectively.

For obtaining analysis of soil moisture, use GET /api/v1/dataset/{dataset_id}/analysis request. 

# Contribution
Please contact the maintainer of this repository

# License
[European Union Public License 1.2](https://github.com/openagri-eu/irrigation-management/blob/main/LICENSE)
