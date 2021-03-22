from flask_restful import Resource, reqparse
from models.course import CourseModel
import datetime

class Course(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=int,
                        required=True,
                        )
    parser.add_argument('on_discount',
                        type=int,
                        required=True,
                        )
    parser.add_argument('discount_price',
                        type=int,
                        required=True,
                        )
    parser.add_argument('description',
                        type=str,
                        required=False,
                        )
    parser.add_argument('image_path',
                        type=str,
                        required=True,
                        )
    parser.add_argument('title',
                        type=str,
                        required=True,
                        )

    def get(self, _id):
        course = CourseModel.find_by_id(_id)
        if course:
            return course.json()
        return {'message': 'course not found'}, 404

    def post(self, _id):
        data = Course.parser.parse_args()
        print(data)
        course = CourseModel(**data)
        try:
            course.save_to_db()
        except:
            return {"message": "An error occurred inserting the course."}, 500

        return course.json(), 201

    def delete(self, _id):
        course = CourseModel.find_by_id(_id)
        if course:
            course.delete_from_db()
            return {'message': 'course deleted.'}
        return {'message': 'course not found.'}, 404

    def put(self, _id):
        data = Course.parser.parse_args()

        course = CourseModel.find_by_id(_id)

        if course:
            course.price = data['price']
            course.description = data['description']
            course.on_discount = data['on_discount']
            course.title = data['title']
            course.date_updated = datetime.datetime.utcnow()
            course.image_path = data['image_path']

        else:
            course = CourseModel(**data)

        course.save_to_db()

        return course.json()

class CoursePost(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('price',
                        type=int,
                        required=True,
                        )

    parser.add_argument('discount_price',
                        type=int,
                        required=True,
                        )

    parser.add_argument('on_discount',
                        type=int,
                        required=True,
                        )
    parser.add_argument('description',
                        type=str,
                        required=False,
                        )
    parser.add_argument('image_path',
                        type=str,
                        required=True,
                        )
    parser.add_argument('title',
                        type=str,
                        required=True,
                        )
    def post(self):
        data = CoursePost.parser.parse_args()
        print(data)
        course = CourseModel(**data)
        try:
            course.save_to_db()
        except:
            return {"message": "An error occurred inserting the course."}, 500

        return course.json(), 201

class CourseListbyTitle(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('title-words', type=str)


    def get(self):
        data = CourseListbyTitle.parser.parse_args()
        title_words = []
        result = []
        if data['title-words'] != None :
            title_words = data['title-words'].split(',')
        if len(title_words) > 0:
            course = CourseModel.find_by_title(title_words[0])
            if course:
                return ({'courses': list(map(lambda x: x.json(), result))})
            else:
                return {'message': 'No Courses present matching those title keywords.'}, 404
        else:
            return {'courses': list(map(lambda x: x.json(), CourseModel.query.all()))}

        return {'message': 'No Courses present'}, 404


