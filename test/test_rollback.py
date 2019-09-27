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

print(payload)
tasks = [
    {
        "method": "POST",
        "route": "rollback/",
        "output": "id",
        "body": payload,
        "expected": {"code": 201},
    },
    {
        "method": "GET",
        "route": "rollback/{{id['id']}}",
        "expected": {
            "body": {
                "task": "task" + value,
                "name": "Second Task",
                "trigram": "ZUPER",
                "hosts": [
                    {"host_id": 0, "fqdn": "le_1.googole.com"},
                    {"host_id": 1, "fqdn": "le_2.googole.com"},
                    {"host_id": 2, "fqdn": "le_3.googole.com"},
                ],
                "id": Int("{{id['id']}}"),
                "status": "RUNNING",
            }
        },
        "retry": 2,
        "rollback": [{"method": "DELETE", "route": "rollback/{{id['id']}}"}],
    },
]

responce = spintest(url, tasks)
