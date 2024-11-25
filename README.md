#  <img src="https://github.com/quantum-label/quantum_labelling_tool/blob/main/static/img/quantum_icon.png" width="50" style="vertical-align:middle"> QUANTUM - The Health Data Quality Label
  
![Python Version](https://img.shields.io/badge/python-3.11%2B-brightgreen.svg)

## Introduction

The **QUANTUM Data Quality Labelling Tool** is a key component of the **European Health Data Space (EHDS)** initiative, designed to address the challenge of ensuring that health datasets are of high quality, accessible, and interoperable across EU member states. As healthcare data plays an increasingly vital role in research, policy, and innovation, this tool provides a standardized mechanism to evaluate and label the **quality, utility, and maturity** of datasets, supporting stakeholders such as healthcare institutions, research organizations, and policymakers.

## Features

This tool empowers **data holders** by offering functionalities to:

- **Feature 1:** Catalogue and Dataset metadata creation
- **Feature 2:** Assess datasets quality based on a guided evaluation of the QUANTUM key dimensions (such as accuracy, accessibility, and compliance) using your own practices.
- **Feature 3:** Generate and visualise data quality certificates (labels) and dowload them in the healthdata@EU standardized RDF format.
- **Feature 4:** Facilitate compliance with EU-wide quality standards such as [HealthDCAT-AP](https://healthdcat-ap.github.io/), [DCAT](https://www.w3.org/TR/vocab-dcat-3/), [DQV](https://www.w3.org/TR/vocab-dqv/).
- **Feature 5:** Provide a transparent and accessible method for assessing data holders maturity.

Ultimately, the QUANTUM tool aims to foster **trust in health data** across Europe by promoting reliable, reusable datasets that can be confidently shared within the European Health Data Space.

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

## Technology Stack

- **Backend:** Python (Django Framework)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (development) or PostgreSQL (production)


---

## Acknowledgments
- Funded by EU [QUANTUM](https://quantumproject.eu) project
- Developed in collaboration with with Sciensano ([Claudio Proietti Mercuri](mailto:claudio.proiettimercuri@sciensano.be)) and UPV ([Ángel Sánchez García](mailto:WRITE_YOUR_EMAIL))
