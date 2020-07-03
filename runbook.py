from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command,netmiko_send_config
from nornir.plugins.functions.text import print_title, print_result

nr = InitNornir(config_file="config.yaml")

def cdp_map(task):
    r = task.run(task=netmiko_send_command, command_string="show cdp neighbor", use_genie=True)
    task.host["facts"] = r.result
    outer = task.host["facts"]
    indexer =outer["cdp"]['index']
    for idx in indexer:
        local_intf = indexer[idx]['local_interface']
        remote_port = indexer[idx]['port_id']
        remote_id = indexer[idx]['device_id']
        if local_intf != 'GigabitEthernet0/0':
            cdp_config = task.run(netmiko_send_config, name='Automating CDP Network Description',
                                  config_commands=[
                                      'interface '+str(local_intf),
                                      'description ' + str(remote_id) + ' <> ' + str(remote_port)
                                  ])



result = nr.run(task=cdp_map)
print_result(result)
