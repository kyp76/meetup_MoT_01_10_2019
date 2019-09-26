from spintest import spintest
from spintest.types import Int
import random

url = ["http://127.0.0.1:8080/"]

value = str(random.randint(1, 100))

payload = {
    "task": "task" + value,
    "name": "Second Task",
    "trigram": "ZUPER",
    "hosts": [
        {"host_id": 0, "fqdn": "le_1.googole.com"},
        {"host_id": 1, "fqdn": "le_2.googole.com"},
        {"host_id": 2, "fqdn": "le_3.googole.com"},
    ],
}

tasks = [
    {
        "method": "POST",
        "route": "retry/",
        "output": "id",
        "body": {"task": "test_retry"},
        "expected": {"code": 201},
    },
    {
        "method": "GET",
        "route": "retry/{{id['id']}}",
        "expected": {
            "body": {
                "task": "test_retry",
                "id": Int("{{id['id']}}"),
                "status": "INSTALLED",
            }
        },
        "retry": 8,
        "delay": 2,
    },
]

responce = spintest(url, tasks)
