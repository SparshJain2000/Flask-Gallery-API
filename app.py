from flask import Flask, send_from_directory, request
from flask_restful import Api, Resource
from datetime import datetime
from werkzeug.utils import secure_filename

import os
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
    def get(self):
        args = request.args
        if(args.get('id') != None):
            if int(args['id']) > len(images):
                return {"error": "Not Found"}, 404
            return {"image": images[args['id']]}
        else:
            return {"images": images}

    def post(self):
        likes = request.form.get('likes')
        image = request.files.get('image')
        path = f'{str(datetime.timestamp(datetime.now())).split(".")[0]}_{image.filename}'
        image.save(os.path.join('data/images/',
                                secure_filename(path)))
        images[len(images)+1] = {
            'likes': int(likes),
            'image': f'/data/images/{path}'
        }
        return {"images": images}


class File(Resource):
    def get(self, path):
        return send_from_directory('data', path)


api.add_resource(HelloWorld, "/")
api.add_resource(Images, "/api/image/")
api.add_resource(File, "/data/<path:path>")
if __name__ == '__main__':
    app.run(debug=True)
