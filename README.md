# Irrigation service

# Description

The OpenAgri Irrigation service provides the calculation of referent evapotranspiration (ETo) as well as the analysis of \
the soil moisture of parcels/plots of land. \
These functionalities can be used via the REST APIs, which provide these them in a linked data format (using JSON-LD). \
This service conforms to the OpenAgri Common Semantic Model (OCSM).

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

# A list of APIs
A full list of APIs can be viewed [here](https://editor-next.swagger.io/?url=https://gist.githubusercontent.com/vlf-stefan-drobic/bf78e620b5a9c5ea22498fd26edb70e5/raw/b0133afe634660791da12af93d251658e08e834f/gistfile1.txt).

For a more detailed view of the APIs, read API.md.

<h3>Quick start for the ETo:</h3>

A user would input the location of their parcel/plot of land via the POST /api/v1/location/ or POST /api/v1/location/parcel-wkt/ APIs (or multiple parcels). \
The system requests weather data for these locations at around midnight every day. \
Once a user wishes to view ETo values, they may call the POST /api/v1/eto/get-calculations/{location_id} API. \
This API will return a list of calculations, for the given days.

<h3>Example usage for the soil moisture analysis:</h3>

Use POST /api/v1/dataset/ to upload your data to the database.
GET and DELETE requests with the same URL as previously mentioned are for fetching and deleting data from database, respectively.

For obtaining analysis of soil moisture, use GET /api/v1/dataset/{dataset_id}/analysis request. 

# Contribution
Please contact the maintainer of this repository

# License
[European Union Public License 1.2](https://github.com/openagri-eu/irrigation-management/blob/main/LICENSE)
