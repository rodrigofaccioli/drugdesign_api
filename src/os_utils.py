from subprocess import Popen, PIPE


def run_command(command=None):

    process = Popen(command,shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
