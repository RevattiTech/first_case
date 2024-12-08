import asyncio
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from src.core.sploitus import parse_page_exploit
from src.endpoints.auth import auth
from src.endpoints.request import route

app = Flask(__name__)
CORS(app, resources={r"*": {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization"]
}})


swagger = Swagger(app)


app.register_blueprint(route, url_prefix='/api/v1')
app.register_blueprint(auth, url_prefix='/api/v1')



if __name__ == "__main__":
    app.run()
