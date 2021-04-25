import time

import pytest

import main


@pytest.fixture
def client():
	main.app.config['TESTING'] = True
	main.REQUEST_TIMEBOUND = 10
	with main.app.test_client() as client:
		yield client


def test_success(client):
	rv = client.get('/')
	assert b'hello' in rv.data


def test_success_maximum_limitation_times(client):
	for i in range(main.MAXIMUM_REQUEST_PER_WINDOW):
		rv = client.get('/')
		assert b'hello' in rv.data


def test_fail_over_maximum_limitation_times(client):
	for i in range(main.MAXIMUM_REQUEST_PER_WINDOW):
		rv = client.get('/')
		assert b'hello' in rv.data
	rv = client.get('/')
	assert b'Rate limit' in rv.data


def test_success_over_maximum_after_time_window(client):
	for i in range(main.MAXIMUM_REQUEST_PER_WINDOW):
		rv = client.get('/')
		assert b'hello' in rv.data
	time.sleep(12)
	rv = client.get('/')
	assert b'hello' in rv.data
