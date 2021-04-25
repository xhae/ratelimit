import collections
import time

from flask import Flask, session

app = Flask(__name__)
# Should be kept as a secret on somewhere else.
app.secret_key = b'saldkgjdfskghre'

# Queue storing each requests in (request_time, USER_ID) pair.
request_queue = collections.deque()
requests_per_id = {}

USER_ID = 'userid'
REQUEST_TIMEBOUND = 3600  # A time window for request number limitation in seconds.
MAXIMUM_REQUEST_PER_WINDOW = 100  # Maximum number of requests within a time window.


def request_add(request_time, request_user_id):
	request_queue.append((request_time, request_user_id))
	if request_user_id not in requests_per_id:
		requests_per_id[request_user_id] = collections.deque()
	requests_per_id[request_user_id].append(request_time)


def request_remove(request_time, request_user_id):
	assert(request_queue.popleft() == (request_time, request_user_id))
	requests_per_id[request_user_id].popleft()
	if len(requests_per_id[request_user_id]) == 0:
		del requests_per_id[request_user_id]


@app.before_request
def limit_requrest_rate():
	now = time.time()
	if USER_ID not in session:
		session[USER_ID] = now
	user_id = session[USER_ID]

	while len(request_queue) > 0:
		# Check the first element of deque keeping the current deque status.
		request_time, request_user_id = request_queue.popleft()
		request_queue.appendleft((request_time, request_user_id))

		if request_time <= now - REQUEST_TIMEBOUND:
			request_remove(request_time, request_user_id)
		else:
			break

	if user_id in requests_per_id and len(requests_per_id[user_id]) >= MAXIMUM_REQUEST_PER_WINDOW:
		last_request_time = requests_per_id[user_id].popleft()
		requests_per_id[user_id].appendleft(last_request_time)
		return 'Rate limit exceeded. Try again in #%s seconds' % int(last_request_time + REQUEST_TIMEBOUND - now + 1), 429
	
	request_add(now, user_id)
	return None


@app.route('/')
def main():
	return 'hello'
