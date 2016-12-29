import os

def run_command(command=None):
    print command
    if command == None:
        raise("command is empty")
    os.system(command)

def get_spark_command(dic_param):
    path_file = os.path.join(dic_param['path_spark_drugdesign'], dic_param['spark_file'])
    command = dic_param['spark_submit']
    command += " "
    command += path_file
    return command

def get_command_chdir(dic_param):
    command = "cd "
    command += dic_param['path_execution']
    command += " "
    return command

def join_2_commands_to_run(command_1, command_2):
    command = command_1
    command += " && "
    command += command_2
    return command

def check_diretory_exists(dir_2_search):
    return os.path.exists(dir_2_search)

def join_directory(dir1, dir2):
    return os.path.join(dir1, dir2)
