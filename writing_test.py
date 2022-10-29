
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result, print_title
from nornir_utils.plugins.tasks.files import write_file
import ipdb
import getpass
import pathlib
from datetime import date


nr = InitNornir(config_file="config.yaml")

username= input("login: ")
password = getpass.getpass()

nr.inventory.defaults.username = username
nr.inventory.defaults.password = password
nr.inventory.defaults.connection_options['netmiko'].extras['secret'] = password


def back_up_configs(task):
    cmds =['show version']

    config_dir = "folder1"
    date_dir = config_dir + "/" + str(date.today())
    pathlib.Path(config_dir).mkdir(exist_ok=True)
    pathlib.Path(date_dir).mkdir(exist_ok=True)
    for cmd in cmds:
        r = task.run(task=netmiko_send_command, enable = True, command_string = cmd)
        task.run(task=write_file,
                content=r.result,
                filename=str(date_dir) + f"/{task.host}.txt")

results = nr.run(name="Creating Prechecks", task=back_up_configs)
print_result(results)

