# app.py - a minimal flask api using flask_restful
from flask import Flask, request, abort
from flask_restful import Resource, Api
from marshmallow import Schema, fields, ValidationError
import math

app = Flask(__name__)
api = Api(app, prefix='/trigonometry')

class QuerySchema(Schema):
    theta = fields.Float(required=True)

class TriangleSchema(Schema):
    opposite = fields.Float()
    adjacent = fields.Float()
    hypotenuse = fields.Float()
    theta = fields.Float()

class Response(Schema):
    status = fields.String()
    result = fields.Nested(TriangleSchema)

querySchema = QuerySchema()
response = Response()
triangle = TriangleSchema()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'trigonometry world'}

class Sin(Resource):
    def get(self):
        args = request.args
        errors = querySchema.validate(request.args)
        if errors:
            abort(400, str(errors))

        result = math.sin(math.radians(float(args["theta"])))

        return response.dump(dict(status="success", result=result)), 201

class Cos(Resource):
    def get(self):
        args = request.args
        errors = querySchema.validate(request.args)
        if errors:
            abort(400, str(errors))

        result = math.cos(math.radians(float(args["theta"])))

        return response.dump(dict(status="success", result=result)), 201

class Tan(Resource):
    def get(self):
        args = request.args
        errors = querySchema.validate(request.args)
        if errors:
            abort(400, str(errors))

        result = math.tan(math.radians(float(args["theta"])))

        return response.dump(dict(status="success", result=result)), 201

class Calculate(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        try:
            data = triangle.load(json_data)
        except ValidationError as err:
            return err.messages, 422

# sin A = opposite / hypotenuse = a / c
# cos A = adjacent / hypotenuse = b / c
# tan A = opposite / adjacent = a / b

        if ('opposite' in data and 'hypotenuse' in data):
            opposite = data['opposite']
            hypotenuse = data['hypotenuse']
            theta_radians = math.asin(opposite/hypotenuse)
            adjacent = math.cos(theta_radians) * hypotenuse
        elif ('adjacent' in data and 'hypotenuse' in data):
            adjacent = data['adjacent']
            hypotenuse = data['hypotenuse']
            theta_radians = math.acos(adjacent/hypotenuse)
            opposite = math.sin(theta_radians) * hypotenuse
        elif ('opposite' in data and 'adjacent' in data):
            opposite = data['opposite']
            adjacent = data['adjacent']
            theta_radians = math.atan(opposite/adjacent)
            hypotenuse = opposite / math.sin(theta_radians)

        result = triangle.dump(dict(theta=math.degrees(theta_radians),opposite=opposite,adjacent=adjacent,hypotenuse=hypotenuse))
        return response.dump(dict(status="success", result=result)), 201

api.add_resource(HelloWorld, '/')
api.add_resource(Sin, '/sin')
api.add_resource(Cos, '/cos')
api.add_resource(Tan, '/tan')
api.add_resource(Calculate, '/calculate')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
