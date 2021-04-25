import pytest

import main


@pytest.fixture
def client():
	main.app.config['TESTING'] = True
	with main.app.test_client() as client:
		yield client


def test_success(client):
	rv = client.get('/')
	assert b'hello' in rv.data


def test_success_100_times(client):
	for i in range(100):
		rv = client.get('/')
		assert b'hello' in rv.data


def test_fail_101_times(client):
	for i in range(100):
		rv = client.get('/')
		assert b'hello' in rv.data
	rv = client.get('/')
	assert b'Rate limit' in rv.data
