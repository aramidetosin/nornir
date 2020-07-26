#!/usr/bin/python3

import threading
import os
from xml.dom import minidom
from nornir import InitNornir
from nornir.plugins.tasks.networking import netconf_get
from rich import print

nr = InitNornir(config_file="config.yaml")
LOCK = threading.Lock()
CLEAR = "clear"

os.system(CLEAR)
def netconf_mac(task):
    mac_result = task.run(task=netconf_get, path="//config/mac-address")
    mac_resulter = mac_result.result
    mac_elements = minidom.parseString(mac_resulter).getElementsByTagName("mac-address")
    LOCK.acquire()
    print(f"[green]**** {task.host} ***********[/green]\n")
    for mac in mac_elements:
        get_parents = mac.parentNode.parentNode.parentNode
        intertag = get_parents.getElementsByTagName("name")
        for inter in intertag:
            inter_output = inter.firstChild.nodeValue
            mac_output = mac.firstChild.nodeValue
            print(f"{inter_output} Physical Address: [red]{mac_output}[/red]")
    LOCK.release()

results = nr.run(task=netconf_mac)