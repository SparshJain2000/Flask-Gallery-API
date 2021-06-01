from flask import Flask, send_from_directory, request, json
from flask_restful import Api, Resource
from datetime import datetime
from werkzeug.utils import secure_filename

import os
app = Flask(__name__)
api = Api(app)
app.config['DEBUG'] = True

f = open('./data/data.json', 'r')
images = json.load(f)
print(images['1'])


def updateJSON(images):
    with open('./data/data.json', 'w') as outfile:
        json.dump(images, outfile)


class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello World! Welcome to Gallery API 🤗"}


class Images(Resource):
    def get(self):
        args = request.args
        if(args.get('id') != None):
            try:
                id = int(args['id'])
                if int(args['id']) > len(images):
                    return {"error": "Not Found"}, 404
                return {"image": images[args['id']]}
            except:
                return {"error": "Invalid Id"}, 404
        return {"images": images}

    def post(self):
        likes = request.form.get('likes')
        author = request.form.get('author')
        title = request.form.get('title')
        image = request.files.get('image')
        path = f'{str(datetime.timestamp(datetime.now())).split(".")[0]}_{image.filename}'
        image.save(os.path.join('data/images/',
                                secure_filename(path)))
        images[str(len(images)+1)] = {
            'likes': int(likes),
            'image': f'/data/images/{path}',
            'author': author,
            "title": title
        }
        updateJSON(images)
        return {"images": images}


class File(Resource):
    def get(self, path):
        return send_from_directory('data', path)


class Like(Resource):
    def get(self, id):
        if(int(id) > len(images)):
            return {"error": "Not Found"}, 404
        images[id]["likes"] += 1
        updateJSON(images)
        return {"image": images[id]}


api.add_resource(HelloWorld, "/")
api.add_resource(Images, "/api/image/")
api.add_resource(File, "/data/<path:path>")
api.add_resource(Like, "/api/like/<string:id>")

if __name__ == '__main__':
    app.run(debug=True)
