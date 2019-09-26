from flask import Flask
from apis import api

flask_app = Flask(__name__)

api.init_app(flask_app)

flask_app.run(host="0.0.0.0", port=8080, debug=True)
