from flask_restplus import Namespace, Resource, fields
import json
import time

api = Namespace("retry", description=" Retry operations")
retry = api.model(
    "retry", {"task": fields.String(required=True, description="The task details")}
)


class Retry(object):
    def __init__(self):
        self.counter = 0
        self.todos = []
        self.time_creating = 10

    def get(self, id):
        for todo in self.todos:
            if todo["id"] == id:
                todo["status"] = "RUNNING"
                if todo["created_time"] + self.time_creating < time.time():
                    todo["status"] = "INSTALLED"
                ret = todo.copy()
                del ret["created_time"]
                return ret

        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo["id"] = self.counter = self.counter + 1
        todo["created_time"] = time.time()
        self.todos.append(todo)
        ret = todo.copy()
        del ret["created_time"]
        return ret


DAO = Retry()
DAO.create({"task": "Create"})


@api.route("/")
class Retry(Resource):
    """Shows a Retry"""

    @api.doc("create_compare")
    @api.expect(retry)
    def post(self):
        """Create a new task"""
        return DAO.create(api.payload), 201


@api.route("/<int:id>")
class RetryID(Resource):
    @api.doc("Retry")
    def get(self, id):
        """Fetch a given resource"""
        return DAO.get(id)
