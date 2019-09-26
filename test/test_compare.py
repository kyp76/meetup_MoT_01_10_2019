from spintest import spintest
from spintest.types import Int
import random

url = ["http://192.166.201.57:8080/"]

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
        "method": "GET",
        "route": "compare/",
        "expected": {
            "code": 200,
            "body": {
                "compare": [
                    {
                        "task": "task1",
                        "name": "First Task",
                        "trigram": "SUPER",
                        "hosts": [{"host_id": 0, "fqdn": None}],
                        "id": None,
                    }
                ]
            },
            "expected_match": "partial",
        },
    },
    {
        "method": "POST",
        "route": "compare/",
        "output": "id",
        "body": payload,
        "expected": {"code": 201},
    },
    {
        "method": "GET",
        "route": "compare/{{id['id']}}",
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
            }
        },
    },
]

responce = spintest(url, tasks)
