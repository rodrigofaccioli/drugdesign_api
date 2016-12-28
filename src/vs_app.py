from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from os_utils import run_command

#from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'mi4u_vs'
api = Api(app)

class PrepareLibrary(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

#    @jwt_required()
    def post(self, name):

        data = PrepareLibrary.parser.parse_args()
        command = "/home/faccioli/Programs/spark-1.4.1-bin-hadoop2.4/bin/spark-submit /home/faccioli/workspace/drugdesign/virtualscreening/vina/spark/prepare_ligand.py /home/faccioli/Execute/teste_webService/virtual_screening/config.ini"
        print(command)
        run_command(command)
        library = {'name': name}
        return library


api.add_resource(PrepareLibrary, '/preparelibrary/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)