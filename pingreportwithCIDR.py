import os
import time
from datetime import datetime
from rich import print
from subprocess import Popen, DEVNULL
from rich.console import Console
from rich.table import Table
from itertools import zip_longest
from ipaddress import ip_network

def pingreport(cidr):
    startTime = datetime.now()
    clear = "clear"
    os.system(clear)
    localtime = time.asctime(time.localtime(time.time()))
    active_list = []
    inactive_list = []

    print("[green]Welcone to Ping Reporter!!![/green]")
    print("[cyan]Please enter the network you wish to test....[/cyan]")
    print("Example: <192.168.10.0/24>")

    print(f"[magenta]You are scanning subnet {cidr}[/magenta]")


    network = ip_network(cidr)

    cmd_dict = {}

    for ip in network.hosts():
        IP = str(ip)
        cmd_dict[IP] = Popen(['ping', '-c', '4', '-i', '0.2', str(IP)], stdout=DEVNULL)

    while cmd_dict:
        for IP, proc in cmd_dict.items():
            if proc.poll() is not None:
                del cmd_dict[IP]
                if proc.returncode == 0:
                    active_list.append(IP)
                elif proc.returncode == 1:
                    inactive_list.append(IP)
                else:
                    print(f"{IP} ERROR")
                break

    table = Table(title="PING REPORT \n" + localtime)
    table.add_column("Active Hosts", justify="center", style="green")
    table.add_column("Inactive Hosts", justify="center", style="red")

    for active, inactive in zip_longest(active_list, inactive_list):
        table.add_row(active, inactive)
    console = Console()
    console.print(table)
    print(f"We have {len(active_list)} of active devices")
    print(f"We have {len(inactive_list)} available IPs")


def main():
    clear = "clear"
    os.system(clear)
    name = input("\nEnter network to Test: ")
    pingreport(name)

if __name__ == "__main__":
    main()
