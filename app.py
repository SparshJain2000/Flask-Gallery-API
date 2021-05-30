from flask import Flask, send_from_directory, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

images = {
    "1": {
        "image": "./data/images/sunset.jpg",
        "likes": 0,
    },
    "2": {
        "image": "./data/images/scene.jpg",
        "likes": 0,
    }
}


class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello World"}


class Images(Resource):
    def get(self, id):
        return {"image": images[id]}


api.add_resource(HelloWorld, "/")
api.add_resource(Images, "/api/image/<string:id>")

if __name__ == '__main__':
    app.run(debug=True)
