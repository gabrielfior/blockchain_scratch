import pytest
import requests

from app.app import create_app


@pytest.fixture
def app():
    return create_app()

def test_chain_endpoint(client):
    #res = client.get(url_for('chain'))
    res = client.get('chain')
    assert res.status_code == requests.codes.OK
    assert res.json['chain'] is not None

def test_register_node(client):

    # start new client in new port

    # register node of new client
    # check if node is present in list of nodes
    # TODO - IMPLEMENT ME!
    assert False

def test_resolve_conflict(client):

    # start new client in new port
    # register node of new client
    # mine 4 blocks in new node
    # trigger /nodes/resolve of initial node
    # assert if chain has been replaced in initial node
    # TODO - IMPLEMENT ME!
    assert False
