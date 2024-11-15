import os
from typing import Optional, Tuple

import requests
import json
from rdflib import Graph, Namespace

FDP_BASE_URL = os.getenv('FDP_URL', 'http://his-fdp-srv-t1.darwinproject.be:8080/')
TOKEN = None


def get_fdp_token() -> Optional[str]:
    """
    Authenticate with the FDP server and return a token.
    """
    URL_token = f'{FDP_BASE_URL}/tokens'
    data = json.dumps(
        {
            'email': os.getenv('FDP_EMAIL', 'claudio.proiettimercuri@sciensano.be'),
            'password': os.getenv('FDP_PASSWORD', 'pasta')
        }
    )
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.post(url=URL_token, data=data, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        return token_data.get('token')
    else:
        print(f'Failed to get token. Status code: {response.status_code}, Message: {response.text}')
        return None


def create_catalogue(rdf_content: str) -> Optional[str]:
    """
    Create a catalogue on the FDP server and return the catalogue ID.
    """
    token = get_fdp_token()
    URL_catalog = f'{FDP_BASE_URL}/catalog'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'text/turtle'
    }
    response = requests.post(url=URL_catalog, data=rdf_content, headers=headers)

    if response.status_code == 201:
        catalog_url = response.headers.get('Location')
        catalogue_id = catalog_url.split('/')[-1] if catalog_url else None
        return catalogue_id
    else:
        print(f'Failed to create catalog. Status code: {response.status_code}, Message: {response.text}')
        return None


def publish_catalogue(catalogue_id: str) -> tuple[int, str]:
    """
    Publish a catalogue on the FDP server by changing its state to "PUBLISHED".
    """
    token = get_fdp_token()
    URL_pub = f'{FDP_BASE_URL}/{catalogue_id}/meta/state'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/json'
    }
    data = json.dumps({'current': 'PUBLISHED'})

    response = requests.put(URL_pub, data=data, headers=headers)

    return response.status_code, response.text


def create_dataset(rdf_content: str) -> Optional[str]:
    """
    Create a dataset on the FDP server and return the dataset ID.
    """
    token = get_fdp_token()
    URL_dataset = f"{FDP_BASE_URL}/dataset"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'text/turtle'
    }

    response = requests.post(url=URL_dataset, data=rdf_content, headers=headers)

    if response.status_code == 201:
        dataset_url = response.headers.get('Location')
        dataset_id = dataset_url.split('/')[-1] if dataset_url else None
        return dataset_id
    else:
        print(f"Failed to create dataset. Status code: {response.status_code}, Message: {response.text}")
        return None


def publish_dataset(dataset_id: str) -> tuple[int, str]:
    """Publishes a dataset by changing its state to 'PUBLISHED'."""
    token = get_fdp_token()
    url = f"{FDP_BASE_URL}/dataset/{dataset_id}/meta/state"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'Content-type': 'application/json'
    }
    data = '{"current":"PUBLISHED"}'

    response = requests.put(url, data=data, headers=headers)

    return response.status_code, response.text


def delete_catalogue(catalogue_id: str, fdp_url: str) -> tuple[int, str]:
    """Deletes a catalogue from the FDP server."""
    token = get_fdp_token()
    url = f'{fdp_url}/catalog/{catalogue_id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    response = requests.delete(url=url, headers=headers)

    return response.status_code, response.text


def delete_dataset(dataset_id: str) -> tuple[int, str]:
    """Deletes a dataset from the FDP server."""
    token = get_fdp_token()
    url = f'{FDP_BASE_URL}/dataset/{dataset_id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    response = requests.delete(url=url, headers=headers)

    return response.status_code, response.text


def modify_catalogue(catalogue_id: str, updated_catalog_data: str) -> tuple[int, str]:
    """Modifies a catalogue's metadata on the FDP server."""
    token = get_fdp_token()
    url = f"{FDP_BASE_URL}/catalog/{catalogue_id}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'text/turtle'
    }

    response = requests.put(url=url, data=updated_catalog_data, headers=headers)

    return response.status_code, response.text


def modify_dataset(dataset_id: str, updated_dataset_data: str) -> tuple[int, str]:
    """Modifies a dataset's metadata on the FDP server."""
    token = get_fdp_token()
    url = f"{FDP_BASE_URL}/dataset/{dataset_id}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'text/turtle'
    }

    response = requests.put(url=url, data=updated_dataset_data, headers=headers)

    return response.status_code, response.text


def create_or_update_quality_certificate(dataset_id: str, certificate_data: str) -> tuple[int, str]:
    """
    Checks if a quality certificate exists for the dataset. If it exists, performs a PUT request to update it.
    Otherwise, performs a POST request to create a new quality certificate.

    Parameters:
    - token: The authentication token for FDP.
    - dataset_uri: URI of the dataset to check for the quality certificate. !!!!!
    - fdp_url: Base URL of the Fair Data Point (FDP).
    - certificate_data: RDF data in Turtle format for the quality certificate.

    Returns:
    - Tuple (status_code, response_text)
    """
    token = get_fdp_token()
    dataset_uri = f'{FDP_BASE_URL}/dataset/{dataset_id}'
    # SPARQL query to check for existing quality certificates
    query = '''
        PREFIX dqv: <http://www.w3.org/ns/dqv#>  
        SELECT ?certificates
        WHERE {
            ?p dqv:hasQualityAnnotation ?certificates .
        }
    '''

    # Parse the dataset URI to check if a quality certificate exists
    graph = Graph()
    graph.parse(dataset_uri)

    # Execute the SPARQL query
    certificate_exists = False
    certificate_id = None

    for result in graph.query(query):
        certificate_id = result['certificates']
        certificate_exists = True
        break

    # Define headers for the request
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'text/turtle'
    }

    # If certificate exists, perform a PUT request to update it
    if certificate_exists:
        # Update the certificate
        url = certificate_id
        response = requests.put(url, data=certificate_data, headers=headers)
    else:
        # If no certificate exists, perform a POST request to create a new certificate
        url = f'{FDP_BASE_URL}/hasQualityAnnotation'
        response = requests.post(url, data=certificate_data, headers=headers)

    return response.status_code, response.text
