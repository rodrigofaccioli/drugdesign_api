import os

path_reference = "/home/faccioli/Execute/teste_webService/virtual_screening"
def run_command(command=None):
    command_exec = "cd "
    command_exec += path_reference
    command_exec += " && "
    command_exec += command
    os.system(command_exec)
