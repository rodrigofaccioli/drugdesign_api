from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from os_utils import run_command, get_spark_command, get_command_chdir, join_2_commands_to_run, check_diretory_exists, join_directory, makedir



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
dic_param['ligand_repository'] = config.get('DRUGDESIGN_API', 'ligand_repository')
dic_param['sufix_dir_for_vs_user'] = config.get('DRUGDESIGN_API', 'sufix_dir_for_vs_user')

class PrepareLibrary(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ligandlib',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

#    @jwt_required()
    def post(self, ligandlib):
        data = PrepareLibrary.parser.parse_args()
        dic_param['spark_file'] = "prepare_ligand.py"

        dir_ligand_repository_param = join_directory(dic_param['ligand_repository'] ,data['ligandlib'])
        if check_diretory_exists(dir_ligand_repository_param) == False:
            mens_ret = "Ligand library needs to be uploaded"

        chdir = get_command_chdir(dic_param)
        spark_command = get_spark_command(dic_param)
        command = join_2_commands_to_run(chdir, spark_command)
        run_command(command)
        mens_ret = "Prepare ligand was executed successfuly"

        mens_ret = {'lig_men': mens_ret}
        return mens_ret

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

class VirtualScreening(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('vsname',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

#    @jwt_required()
    def post(self, vsname):
        data = VirtualScreening.parser.parse_args()
        # Dictionary that contains all mensagens
        mens_res_vs = {}
        mens_res_vs['prepare_dir'] = "Not Performed"
        mens_res_vs['prepare_dock_lis'] = "Not Performed"
        mens_res_vs['perform_vs'] = "Not Performed"

        #Checking directory to perform VS
        dir_for_perform_vs = join_directory(dic_param['path_execution'] ,data['vsname'])
        if check_diretory_exists(dir_for_perform_vs) == False:
            makedir(dir_for_perform_vs)
        mens_res_vs['prepare_dir'] = "It was performed with success"

        #Preparing list docking
        dic_param['spark_file'] = "prepare_docking_list.py"
        chdir = get_command_chdir(dic_param)
        spark_command = get_spark_command(dic_param)
        spark_command += " "
        spark_command += dic_param['path_execution'] #sys.argv[1] required by prepare_docking_list.py
        command = join_2_commands_to_run(chdir, spark_command)
        run_command(command)
        mens_res_vs['prepare_dock_lis'] = "It was performed with success"

        #Perform Virtual screening
        dic_param['spark_file'] = "vina_docking.py"
        chdir = get_command_chdir(dic_param)
        spark_command = get_spark_command(dic_param)
        spark_command += " "
        path_file_docking_list = join_directory(dic_param['path_execution'], "docking_list.txt")
        spark_command +=  path_file_docking_list #sys.argv[1] required by prepare_vina_docking.py
        command = join_2_commands_to_run(chdir, spark_command)
        run_command(command)
        mens_res_vs['perform_vs'] = "It was performed with success"

        return mens_res_vs

class VirtualScreeningAnalysis(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('vsname',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('probe',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('ndots',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('distanceCutoff',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('angleCutoff',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

#    @jwt_required()
    def post(self, vsname, probe, ndots, distanceCutoff, angleCutoff):
        data = VirtualScreeningAnalysis.parser.parse_args()
        # Dictionary that contains all mensagens
        mens_res_vs_ana = {}
        mens_res_vs_ana['error_mes_vs_ana'] = "None"
        mens_res_vs_ana['create_file_for_analysis'] = "Not Performed"
        mens_res_vs_ana['prepare_files_for_analysis'] = "Not Performed"
        mens_res_vs_ana['ligand_efficiency'] = "Not Performed"
        mens_res_vs_ana['computing_burried_area_total'] = "Not Performed"
        mens_res_vs_ana['computing_burried_area_of_receptor_and_all_residues'] = "Not Performed"
        mens_res_vs_ana['computing_burried_area_of_ligand'] = "Not Performed"
        mens_res_vs_ana['hydrogen_bond'] = "Not Performed"
        mens_res_vs_ana['full_data_analysis'] = "Not Performed"

        #Checking directory of Virtual Screening that must be Performed
        dir_for_vs_analysis = join_directory(dic_param['path_execution'],dic_param['sufix_dir_for_vs_user'])
        dir_for_vs_analysis = join_directory(dir_for_vs_analysis, data['vsname'])

        if check_diretory_exists(dir_for_vs_analysis) == False:
            mens = dir_for_vs_analysis
            mens = " "
            mens += "VS for analysis directory not found"
            mens_res_vs_ana['error_mes_vs_ana'] = mens
        else: #able for performing analysis

            # Create file for analysis
            dic_param['spark_file'] = "create_file_for_analysis.py"
            chdir = get_command_chdir(dic_param)
            spark_command = get_spark_command(dic_param)
            command = join_2_commands_to_run(chdir, spark_command)
            run_command(command)
            mens_res_vs_ana['create_file_for_analysis'] = "Performed with success"

            # Prepare files for analysis
            dic_param['spark_file'] = "prepare_files_for_analysis.py"
            chdir = get_command_chdir(dic_param)
            spark_command = get_spark_command(dic_param)
            command = join_2_commands_to_run(chdir, spark_command)
            run_command(command)
            mens_res_vs_ana['prepare_files_for_analysis'] = "Performed with success"

            # Ligand efficiency
            dic_param['spark_file'] = "ligand_efficiency.py"
            chdir = get_command_chdir(dic_param)
            spark_command = get_spark_command(dic_param)
            command = join_2_commands_to_run(chdir, spark_command)
            run_command(command)
            mens_res_vs_ana['ligand_efficiency'] = "Performed with success"

            # Computing_burried_area_total
            dic_param['spark_file'] = "buried_areas.py"
            chdir = get_command_chdir(dic_param)
            spark_command = get_spark_command(dic_param)
            spark_command += " "
            spark_command += str(data['probe'])
            spark_command += " "
            spark_command += str(data['ndots'])
            command = join_2_commands_to_run(chdir, spark_command)
            run_command(command)
            mens_res_vs_ana['computing_burried_area_total'] = "Performed with success"

            # Computing burried area of receptor and all residues
            dic_param['spark_file'] = "buried_area_receptor.py"
            chdir = get_command_chdir(dic_param)
            spark_command = get_spark_command(dic_param)
            command = join_2_commands_to_run(chdir, spark_command)
            run_command(command)
            mens_res_vs_ana['computing_burried_area_of_receptor_and_all_residues'] = "Performed with success"

            # Computing burried are of ligand
            dic_param['spark_file'] = "buried_area_ligand.py"
            chdir = get_command_chdir(dic_param)
            spark_command = get_spark_command(dic_param)
            spark_command += " "
            spark_command += str(data['probe'])
            spark_command += " "
            spark_command += str(data['ndots'])
            command = join_2_commands_to_run(chdir, spark_command)
            run_command(command)
            mens_res_vs_ana['computing_burried_area_of_ligand'] = "Performed with success"

            # Hydrogen bond
            dic_param['spark_file'] = "hydrogen_bond.py"
            chdir = get_command_chdir(dic_param)
            spark_command = get_spark_command(dic_param)
            spark_command += " "
            spark_command += str(data['distanceCutoff'])
            spark_command += " "
            spark_command += str(data['angleCutoff'])
            command = join_2_commands_to_run(chdir, spark_command)
            run_command(command)
            mens_res_vs_ana['hydrogen_bond'] = "Performed with success"

            # Full data analysis
            dic_param['spark_file'] = "vs_full_data_analysis.py"
            chdir = get_command_chdir(dic_param)
            spark_command = get_spark_command(dic_param)
            command = join_2_commands_to_run(chdir, spark_command)
            run_command(command)
            mens_res_vs_ana['full_data_analysis'] = "Performed with success"

        return mens_res_vs_ana

api.add_resource(PrepareLibrary, '/preparelibrary/<string:ligandlib>')
api.add_resource(PrepareReceptor, '/preparereceptor/<string:receptor>')
api.add_resource(VirtualScreening, '/vs/<string:vsname>')
api.add_resource(VirtualScreeningAnalysis,'/vsana/<string:vsname>/<float:probe>/<int:ndots>/<float:distanceCutoff>/<float:angleCutoff>')

if __name__ == '__main__':
    app.run(debug=True)
