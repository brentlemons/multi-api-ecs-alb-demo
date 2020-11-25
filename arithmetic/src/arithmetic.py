# app.py - a minimal flask api using flask_restful
from flask import Flask, request, abort
from flask_restful import Resource, Api
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
api = Api(app, prefix='/arithmetic')

class SimpleSchema(Schema):
    a = fields.Float()
    b = fields.Float()

class Response(Schema):
    status = fields.String()
    result = fields.Float()

simple_schema = SimpleSchema()
response = Response()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'arithmetic world'}

class Addition(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = simple_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        result = data["a"] + data["b"]

        return response.dump(dict(status="success", result=result)), 201

class Subtraction(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = simple_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        result = data["a"] - data["b"]

        return response.dump(dict(status="success", result=result)), 201

class Multiplication(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = simple_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        result = data["a"] * data["b"]

        return response.dump(dict(status="success", result=result)), 201

class Division(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = simple_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        result = data["a"] / data["b"]

        return response.dump(dict(status="success", result=result)), 201


api.add_resource(HelloWorld, '/')
api.add_resource(Addition, '/add')
api.add_resource(Subtraction, '/subtract')
api.add_resource(Multiplication, '/multiply')
api.add_resource(Division, '/divide')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

