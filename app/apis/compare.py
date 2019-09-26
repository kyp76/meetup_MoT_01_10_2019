from flask_restplus import Namespace, Resource, fields
import json

api = Namespace("compare", description=" Route operations")
compare = api.model(
    "compare", {"task": fields.String(required=True, description="The task details")}
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


payload = {
    "task": "task1",
    "name": "First Task",
    "trigram": "SUPER",
    "hosts": [{"host_id": 0, "fqdn": "le_beau_gosse.googole.com"}],
}

DAO = TodoDAO()
DAO.create(payload)


@api.route("/")
class CompareList(Resource):
    """Shows a list of all Compare, and lets you POST to add new tasks"""

    @api.doc("list_compare")
    def get(self):
        """List all tasks"""
        return {"compare": DAO.todos}

    @api.doc("create_compare")
    @api.expect(compare)
    def post(self):
        """Create a new task"""
        return DAO.create(api.payload), 201


@api.route("/<int:id>")
@api.response(404, "compare not found")
@api.param("id", "The task identifier")
class Compare(Resource):
    """Show a single compare item and lets you delete them"""

    @api.doc("get_compare")
    def get(self, id):
        """Fetch a given resource"""
        return DAO.get(id)

    @api.doc("delete_compare")
    @api.response(204, "Compare deleted")
    def delete(self, id):
        """Delete a task given its identifier"""
        DAO.delete(id)
        return "", 204

    @api.expect(compare)
    def put(self, id):
        """Update a task given its identifier"""
        return DAO.update(id, api.payload)
