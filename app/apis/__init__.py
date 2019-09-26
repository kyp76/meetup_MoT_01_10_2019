from flask_restplus import Api

from .compare import api as ns1
from .retry import api as ns2
from .rollback import api as ns3

api = Api(
    version="1.0",
    title="Name Recorder",
    description="Manage names of various users of the application",
)

api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
