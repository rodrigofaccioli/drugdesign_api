from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from os_utils import run_command, get_spark_command, get_command_chdir, join_2_commands_to_run



#from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'mi4u_vs'
api = Api(app)

import ConfigParser as configparser
config = configparser.ConfigParser()
config.read('config.ini')
dic_param = {}
dic_param['path_spark_drugdesign'] = config.get('DRUGDESIGN', 'path_spark_drugdesign')
dic_param['path_execution'] = config.get('DRUGDESIGN_API', 'path_execution')
dic_param['spark_submit'] = config.get('DRUGDESIGN_API', 'spark_submit')


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
#        print data['name']
        dic_param['spark_file'] = "prepare_ligand.py"

        chdir = get_command_chdir(dic_param)
        spark_command = get_spark_command(dic_param)
        command = join_2_commands_to_run(chdir, spark_command)
        run_command(command)

        library = {'name': command}
        return library

api.add_resource(PrepareLibrary, '/preparelibrary/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
