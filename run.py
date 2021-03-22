from flask import Flask
from flask_restful import Api
import json
import os


from resources.course import Course, CoursePost,CourseListbyTitle
from models.course import CourseModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()
    loadJson()

api.add_resource(Course, '/course/<int:_id>')
api.add_resource(CoursePost, '/course')
api.add_resource(CourseListbyTitle, '/course/')

def loadJson():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + '\course.json'
    f = open(file_path)
    data = json.load(f)
    for obj in data:
        args = {'description': obj["description"], 'discount_price': obj["discount_price"],
                'image_path': obj["image_path"], 'on_discount': obj["on_discount"], 'price': obj["price"], 'title': obj["title"]}
        course = CourseModel(**args)
        CourseModel.add_data_to_db(course)
    f.close()

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
