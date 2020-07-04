from flask import Flask, request, jsonify
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, fields
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, verify_jwt_in_request
)
from flask_jwt_extended.exceptions import NoAuthorizationError

app = Flask(__name__)
# app.config['JWT_TOKEN_LOCATION'] = ['query_string']
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['PROPAGATE_EXCEPTIONS'] = True
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'authorization'
    }
}
api = Api(app, version='1.0', title='Team 12 Dispatcher APIs',
          description='', authorizations=authorizations, security='apikey'
          )
ns = api.namespace('devices', description='Rubbish device operations')
jwt = JWTManager(app)

slot_sensor_model = api.model('SlotSensorDevice', {
    'serialNo': fields.String(required=True, description='serial number sensor'),
    'modelNo': fields.String(required=True, description='model sensor'),
    'brand': fields.String(required=True, description='brand sensor'),
    'code': fields.String(required=True, description='team12 code sensor'),
    'statusCode': fields.String(required=True, description='team12 status code'),
    'note': fields.String(required=False, description='team12 status code'),
})

slot_rubbish_model = api.model('SlotRubbishDevice', {
    'actualWeight': fields.Float(required=True, description='Slot actual weight'),
    'previousWeight': fields.Float(required=True, description='Slot previous weight'),
    'decimalLongitude': fields.Float(required=True, description='bin longitude'),
    'decimalLatitude': fields.Float(required=True, description='bin latitude'),
    'hookingCode': fields.String(required=True, description='Code to match with user multimedial file'),
    'sensorInfo': fields.Nested(model=slot_sensor_model, required=True, description='Sensor information')
})


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'brunello' or password != 'SB2uyRpApwWp8znr':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@ns.route('/rubbish/<string:id>/slot/<string:type_slot>/telemetry')
class RubbishDevice(Resource):
    @ns.expect(slot_rubbish_model, validate=True)
    @jwt_required
    def post(self, id, type_slot):
        json_data = request.json
        if not json_data:
            return ({'error': 'JSON is empty'}, 400)
        return ('', 204)

@api.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return {'message': str(e)}, 401
