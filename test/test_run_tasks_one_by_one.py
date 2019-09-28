import asyncio
from spintest import TaskManager
import os
import json

url = ["http://127.0.0.1:8080/"]

payload = {"task": "task written through API"}


tasks = [
    {
        "method": "POST",
        "route": "one_by_one/",
        "output": "id",
        "body": payload,
        "expected": {"code": 201},
    },
    {
        "method": "GET",
        "route": "one_by_one/{{id['id']}}",
        "expected": {"body": {"one_by_one": payload}},
    },
]
loop = asyncio.get_event_loop()
manager = TaskManager(url, tasks)

fake_payload = {"toto": "FAKE"}


def read_file(id):
    with open(os.environ["HOME"] + "/tmp/meetup.txt", "r") as f:
        result = f.read()
        payload["id"] = id
        if result == str(payload):
            # if result == str(fake_payload):
            return True
        else:
            raise Exception


result1 = loop.run_until_complete(manager.next())
print(result1)
result2 = read_file(result1["body"]["id"])
print(result2)
if result2:
    result3 = loop.run_until_complete(manager.next())
