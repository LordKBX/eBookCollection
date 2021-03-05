import os, sys
import subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common.vars import *


def inflate(src: str, dest: str):
    list_args = list()  # create list argument for external command execution
    list_args.append(env_vars['tools']['archiver']['path'] + os.sep + env_vars['tools']['archiver'][os.name]['exe'])  # insert executable path
    temp_args = env_vars['tools']['archiver'][os.name]['params_inflate'].split(' ')  # create table of raw command arguments
    for var in temp_args:  # parse table of raw command arguments
        # insert parsed param
        list_args.append(var.replace('%input%', src).replace('%output%', dest))
    # print(list_args)
    return subprocess.check_output(list_args, universal_newlines=True)  # execute the command


def deflate(src: str, dest: str):
    list_args = list()  # create list argument for external command execution
    list_args.append(env_vars['tools']['archiver']['path'] + os.sep + env_vars['tools']['archiver'][os.name]['exe'])  # insert executable path
    temp_args = env_vars['tools']['archiver'][os.name]['params_deflate'].split(' ')  # create table of raw command arguments
    for var in temp_args:  # parse table of raw command arguments
        # insert parsed param
        list_args.append(var.replace('%input%', src).replace('%output%', dest))
    print(list_args)
    ret = subprocess.check_output(list_args, universal_newlines=True)  # execute the command
    print(ret)
    return ret
