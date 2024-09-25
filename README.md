# Irrigation service

# Description

The Irrigation service takes in data via datasets and \
returns the results of the ETo or soil moisture analysis

# Requirements

<ul>
    <li>git</li>
    <li>docker</li>
</ul>

Docker version used during development: 27.0.3

# Installation

There are two ways to install this service, via docker or directly from source.

<h3> Deploying from source </h3>

When deploying from source, use python 3:11.\
Also, you should use a [venv](https://peps.python.org/pep-0405/) when doing this.

A list of libraries that are required for this service is present in the "requirements.txt" file.\
This service uses FastAPI as a web framework to serve APIs, alembic for database migrations sqlalchemy for database ORM mapping.

<h3> Deploying via docker </h3>

After installing <code> docker </code> you can run the following commands to run the application:

```
docker build -t irrigation .
docker run -d --name irrigation -p 80:80 irrigation
```

The application will be served on http://127.0.0.1:80 (I.E. typing localhost/docs in your browser will load the swagger documentation)

# Documentation

Examples:
<h3>POST</h3>
/api/v1/eto/

<h3> Example usage </h3>

In order to use the aforementioned API, you need to fill out the input parameters corresponding to the requested ETO calculation.

# Contribution
Please contact the maintainer of this repository

# License
[European Union Public License 1.2](https://github.com/openagri-eu/irrigation-management/blob/main/LICENSE)
