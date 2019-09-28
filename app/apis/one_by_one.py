import os
from flask_restplus import Namespace, Resource, fields

api = Namespace("one_by_one", description=" Route operations")
one_by_one = api.model(
    "one_by_one", {"task": fields.String(required=True, description="The task details")}
)


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo["id"] == id:
                return {"one_by_one": todo}
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo["id"] = self.counter = self.counter + 1
        self.todos.append(todo)
        with open(os.environ["HOME"] + "/tmp/meetup.txt", "w") as f:
            f.write(str(todo))
            f.close()
        return todo


#
#    def update(self, id, data):
#        todo = self.get(id)
#        todo.update(data)
#        return todo
#
#    def delete(self, id):
#        todo = self.get(id)
#        self.todos.remove(todo)
#

DAO = TodoDAO()


@api.route("/")
class OneByOneList(Resource):
    """Shows a list of all OneByOne, and lets you POST to add new tasks"""

    #    @api.doc("list_one_by_one")
    #    def get(self):
    #        """List all tasks"""
    #        return {"one_by_one": DAO.todos}
    #
    @api.doc("create_one_by_one")
    @api.expect(one_by_one)
    def post(self):
        """Create a new task"""
        return DAO.create(api.payload), 201


@api.route("/<int:id>")
@api.response(404, "one_by_one not found")
@api.param("id", "The task identifier")
class OneByOne(Resource):
    """Show a single one_by_one item and lets you delete them"""

    @api.doc("get_one_by_one")
    def get(self, id):
        """Fetch a given resource"""
        return DAO.get(id)


#    @api.doc("delete_one_by_one")
#    @api.response(204, "OneByOne deleted")
#    def delete(self, id):
#        """Delete a task given its identifier"""
#        DAO.delete(id)
#        return "", 204
#
#    @api.expect(one_by_one)
#    def put(self, id):
#        """Update a task given its identifier"""
#        return DAO.update(id, api.payload)
