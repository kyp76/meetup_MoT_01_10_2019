from flask_restplus import Namespace, Resource, fields
import json

api = Namespace("rollback", description=" Rollback operations")
rollback = api.model(
    "rollback",
    {
        "id": fields.Integer(readOnly=True, description="The task unique identifier"),
        "task": fields.String(required=True, description="The task details"),
        #"status": fields.String(required=True, description="The status details"),
    },
)


class Rollback(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo["id"] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo["id"] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo


DAO = Rollback()
DAO.create({'task': 'Create', "status": "RUNNING"})


@api.route("/")
class Rollback(Resource):
    """Shows a Rollback"""

    @api.doc("Rollback")
    @api.marshal_list_with(rollback)
    def get(self):
        """List all tasks"""
        return json.dump(DAO.compares)

    @api.doc("create_rollback")
    @api.expect(rollback)
    @api.marshal_with(rollback, code=201)
    def post(self):
        """Create a new task"""
        return DAO.create(api.payload), 201

