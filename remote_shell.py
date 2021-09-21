import paramiko
import time
import os
from rich.console import Console
from rich.text import Text
from rich.prompt import Prompt

console = Console()


def colour_print(colour, string):
    console.print(string, style = f'bold {colour}')


def connect(hostname, port, username, password):
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	colour_print("#FFFFFF", "Connecting.............")
	ssh_client.connect(hostname=hostname, port=port,username=username, password=password)
	return ssh_client


def get_shell(ssh_client):
	shell = ssh_client.invoke_shell()
	return shell


def send_cmd(shell,cmd):
	colour_print("#FFFFFF", f"Sending...{cmd}")
	shell.send(cmd+"\n")
	time.sleep(1)


def show(shell):
	output = shell.recv(10000)
	return output.decode("utf-8")


def close(ssh_client):
	if ssh_client.get_transport().is_active() == True:
		colour_print("#FFFFFF", "Disconnecting.............")
	ssh_client.close()


def menu():
	colour_print("green", "1. Display uptime")
	colour_print("green","2. Disk free details")
	colour_print("green","3. Display available RAM")
	colour_print("green","4. List directory content")
	colour_print("red","5.Exit")


if __name__ == "__main__":

	client=connect("127.0.0.1",22,"veena","root123")
	shell=get_shell(client)

	while True:
		menu()
		ch = Prompt.ask("Enter your option:	", choices=[str(x) for x in range(1,6)])
		if ch == "1":
			send_cmd(shell,"uptime")
			console.print("#FF00FF", show(shell))
		elif ch == "2":
			send_cmd(shell,"df")
			colour_print("#FF00FF", show(shell))
		elif ch == "3":
			send_cmd(shell,"free -m")
			colour_print("#FF00FF", show(shell))
		elif ch == "4":
			send_cmd(shell,"ls /home/veena/Python_Training_UST/")
			colour_print("#FF00FF", show(shell))
		elif ch == "5":
			break
	#close(shell)
