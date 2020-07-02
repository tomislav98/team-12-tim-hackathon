from flask import Flask, request
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Team 12 Dispatcher APIs',
    description='',
)

slot_sensor_model = api.model('SlotSensorDevice', {
    'serialNo' : fields.String(required=True, description='serial number sensor'),
    'modelNo' : fields.String(required=True, description='model sensor'),
    'brand' : fields.String(required=True, description='brand sensor'),
    'code' : fields.String(required=True, description='team12 code sensor'),
    'statusCode' : fields.String(required=True, description='team12 status code'),
    'note' : fields.String(required=False, description='team12 status code'),
})


slot_rubbish_model = api.model('SlotRubbishDevice', {
    'actualWeight': fields.Float(required=True, description='Slot actual weight'),
    'previousWeight': fields.Float(required=True, description='Slot previous weight'),
    'decimalLongitude' : fields.Float(required=True, description='bin longitude'),
    'decimalLatitude' : fields.Float(required=True, description='bin latitude'),
    'hookingCode' : fields.String(required=True, description='Code to match with user multimedial file'),
    'sensorInfo' : fields.Nested(model=slot_sensor_model, required=True, description='Sensor information')
})


ns = api.namespace('devices', description='Rubbish device operations')
@ns.route('/rubbish/<string:id>/slot/<string:type_slot>/telemetry')
class RubbishDevice(Resource):
    @ns.expect(slot_rubbish_model, validate=True)
    def post(self, id, type_slot):
        json_data = request.json
        if not json_data:
            return ({'error' : 'JSON is empty'}, 400)
        print(json_data)
        return ('', 204)

if __name__ == '__main__':
    app.run(debug=False)
