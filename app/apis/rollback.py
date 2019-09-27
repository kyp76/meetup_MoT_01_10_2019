from flask_restplus import Namespace, Resource, fields
import json

api = Namespace("rollback", description=" Route operations")
rollback = api.model(
    "rollback", {"task": fields.String(required=True, description="The task details")}
)


class TodoDAO(object):
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
        todo["status"] = "ERROR"
        todo["id"] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()


@api.route("/")
class RollbackList(Resource):
    """Shows a list of all Rollback, and lets you POST to add new tasks"""

    @api.doc("create_rollback")
    @api.expect(rollback)
    def post(self):
        """Create a new task"""
        return DAO.create(api.payload), 201


@api.route("/<int:id>")
@api.response(404, "rollback not found")
@api.param("id", "The task identifier")
class Rollback(Resource):
    """Show a single rollback item and lets you delete them"""

    @api.doc("get_rollback")
    def get(self, id):
        """Fetch a given resource"""
        return DAO.get(id)

    @api.doc("delete_rollback")
    @api.response(204, "Rollback deleted")
    def delete(self, id):
        """Delete a task given its identifier"""
        DAO.delete(id)
        return "", 204
