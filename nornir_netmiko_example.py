
from unicodedata import name
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result, print_title
from nornir_utils.plugins.tasks.files import write_file
from nornir_utils.plugins.tasks.networking import tcp_ping
from nornir.core.filter import F
import ipdb
import getpass


nr = InitNornir(config_file="config.yaml")

username= input("login: ")
password = getpass.getpass()

nr.inventory.defaults.username = username
nr.inventory.defaults.password = password
nr.inventory.defaults.connection_options['netmiko'].extras['secret'] = password

acc= nr.filter(mdf= True)

cmds =['show ip int br', 'sh int status']
def nugget_test(task):
    for cmd in cmds:
        version_result = task.run(task=netmiko_send_command, enable=True, command_string = cmd, name=cmd)


r = acc.run(task=nugget_test)
# r = acc.run(task=ping_test)
if __name__ == "__main__":
    print_result(r)
    # ipdb.set_trace()