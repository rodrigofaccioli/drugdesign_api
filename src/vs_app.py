from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from os_utils import run_command, get_spark_command, get_command_chdir, join_2_commands_to_run, check_diretory_exists, join_directory



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
dic_param['receptor_repository'] = config.get('DRUGDESIGN_API', 'receptor_repository')


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

class PrepareReceptor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('receptor',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

#    @jwt_required()
    def post(self, receptor):
        data = PrepareReceptor.parser.parse_args()
        dic_param['spark_file'] = "prepare_receptor.py"

        dir_repository_param = join_directory(dic_param['receptor_repository'] ,data['receptor'])
        if check_diretory_exists(dir_repository_param) == False:
            mens_ret = "PDB Receptor(es) need to be uploaded"

        chdir = get_command_chdir(dic_param)
        spark_command = get_spark_command(dic_param)
        command = join_2_commands_to_run(chdir, spark_command)
        run_command(command)
        mens_ret = "Prepare receptor was executed successfuly"

        mens_ret = {'men_receptor': mens_ret}
        return mens_ret

api.add_resource(PrepareLibrary, '/preparelibrary/<string:name>')
api.add_resource(PrepareReceptor, '/preparereceptor/<string:receptor>')

if __name__ == '__main__':
    app.run(debug=True)
