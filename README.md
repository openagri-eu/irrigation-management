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

There are two ways to install this service, via docker (prefered) or directly from source.

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

<h3>Example Usage for the ETo:</h3>

A user would input the location of their parcel/plot of land via the POST /api/v1/location/ API (or multiple parcels). \
The system requests weather data for these locations at around midnight every day. \
Once a user wishes to view ETo values, they may call the POST /api/v1/eto/get-calculations/{location_id} API. \
This API will return a list of calculations, for the given days.

Currently, because the service only starts collecting data once it has been deployed, it is not possible to \
query for ETo values for days before it has been deployed.

# Contribution
Please contact the maintainer of this repository

# License
[European Union Public License 1.2](https://github.com/openagri-eu/irrigation-management/blob/main/LICENSE)
