import os
import time
from datetime import datetime
import yaml
from subprocess import Popen, DEVNULL
from rich.console import Console
from rich.table import Table
from itertools import zip_longest
import sys

def pingreport(filename):
    startTime = datetime.now()
    clear = "clear"
    os.system(clear)
    localtime = time.asctime(time.localtime(time.time()))
    active_list = []
    inactive_list = []

    cmd_dict = {}

    with open(filename) as f:
        file = yaml.load(f, Loader=yaml.FullLoader)
    ip_list = []

    for k, v in file.items():
        ips = v["hostname"]
        ip_list.append(ips)

    for ip in ip_list:
        cmd_dict[ip] = Popen(['ping', '-c', '4', '-i', '0.2', ip], stdout=DEVNULL)

    while cmd_dict:
        for ip, proc in cmd_dict.items():
            if proc.poll() is not None:
                del cmd_dict[ip]
                if proc.returncode == 0:
                    active_list.append(ip)
                elif proc.returncode == 1:
                    inactive_list.append(ip)
                else:
                    print(f"{ip} ERROR")
                break

    table = Table(title="PING REPORT \n" + localtime)
    table.add_column("Active Hosts", justify="center", style="green")
    table.add_column("Inactive Hosts", justify="center", style="red")

    for active, inactive in zip_longest(active_list, inactive_list):
        table.add_row(active, inactive)
    console = Console()
    console.print(table)
    print(datetime.now() - startTime)


def main():
    name = sys.argv[1]
    pingreport(name)

if __name__ == "__main__":
    main()
