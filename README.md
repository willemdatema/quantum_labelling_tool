# QUANTUM labelling tool
  
![Python Version](https://img.shields.io/badge/python-3.11%2B-brightgreen.svg)

`QUANTOM labelling tool` is a web application designed to the data quality, utility and maturity assessment of data holders' datasets.

## Features

- **Feature 1:** Catalogue and Dataset metadata creation
- **Feature 2:** Data quality assessment of datasets
- **Feature 3:** Data Quality Label and RDF creation
- **Feature 4:** Organization maturity assessment

## Requirements

Python 3.11

## Installation for use
Clone the repository and then:
```bash
cd [repository_directory]
pip install -r requirements.txt
python manage.py createsuperuser # for creating root user if wanted 
```

## Usage

```bash
python manage.py runserver 0.0.0.0:8000
```

- Access localhost:8000 to continue
- Access localhost:8000/admin to visit the Admin dashboard (login is root for user and password)
- To register a user it is needed to 1) create the user, 2) create an organization, 3) relate a user with an organization (userorganization)

---

Made by [QUANTUM](https://quantumproject.eu)
