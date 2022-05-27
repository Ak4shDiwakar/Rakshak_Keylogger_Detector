#!/usr/bin/env python
from ast import For
import importlib
import shlex
import subprocess
from os.path import exists
import psutil
import getopt
import sys
import os.path
import easygui
from colorama import Fore, Back, Style
from termcolor import colored
from pyfiglet import Figlet

time = 1
black_list = []
white_list = []

short_options = "har"
long_options = ["help", "add-to-startup", "remove-from-startup"]
# remove 1st argument from list of arguments
argumentList = sys.argv[1:]
# autostart directory
autostart_path = os.path.expanduser('~/.config/autostart/')
# arguments dealt with here
if argumentList:
    try:
        arguments, values = getopt.getopt(argumentList, short_options, long_options)
        for opt, arg in arguments:
            if opt in ('-h', "--help"):
                print(Fore.GREEN + 'Available arguments:\n'
                      '-h/--help  Shows this menu\n'
                      '-a/--add-to-startup  Adds program to startup directory\n'
                      '-r/--remove-from-startup  Removes program from startup directory.')
            elif opt in ('-a', "--add-to-startup"):
                # create autostart directory if it does not exist
                start_directory = exists(autostart_path)
                if not start_directory:
                    os.makedirs(autostart_path, mode=0o777, exist_ok=False)
                # check if file already exists in startup
                program_path = exists(os.path.join(autostart_path, 'Rakshak.desktop'))
                if program_path:
                    print(Fore.RED+'Error: Program already exists in startup.')
                else:
                    # create .desktop file to place in startup folder
                    with open(os.path.join(autostart_path, 'Rakshak.desktop'), "w") as file1:
                        toFile = ('[Desktop Entry]\n'
                                  'Version=v0.1\n'
                                  'Type=Application\n'
                                  'Name=Rakshak\n'
                                  f'Exec=python3 {os.getcwd()}/Rakshak.py\n'
                                  'Terminal=true')
                        file1.write(toFile)
                    # give permission to launch
                    st = os.stat(os.path.join(autostart_path, 'Rakshak.desktop'))
                    # only file owner can write to file, others can read - 664
                    os.chmod(os.path.join(autostart_path, 'Rakshak.desktop'), 0o664)
                    check_exists = exists(autostart_path)
                    if check_exists:
                        print(Fore.LIGHTGREEN_EX+"Program successfully added to startup.")
                    else:
                        print(Fore.LIGHTYELLOW_EX+"Program was not added to startup. Please try again.")
            elif opt in ('-r', "--remove-from-startup"):
                program_path = exists(os.path.join(autostart_path, 'Rakshak.desktop'))
                if program_path:
                    os.remove(os.path.join(autostart_path, 'Rakshak.desktop'))
                    program_path = exists(os.path.join(autostart_path, 'Rakshak.desktop'))
                    if not program_path:
                        print(Fore.BLUE+"File removed successfully.")
                    else:
                        print(Fore.LIGHTRED_EX+"Error: File was not removed from startup.")
                else:
                    print(Fore.LIGHTRED_EX+"Error: Program does not exist in startup directory.")

    except getopt.error as err:
        # output error and return error code
        print(str(err))
else:
    
    while True:
        
        if time == 1:
            f=Figlet(font="standard")

            print(colored(f.renderText('Rakshak Anti_keylogger\n'),'green'))
            print(Fore.LIGHTMAGENTA_EX+'-h , -help : for Available arguments\nPress Ctrl+C to exit from Programm')
            print(Fore.CYAN+'\nScanning in progress...')
        command = shlex.split('lsof -nP -iTCP:587 -iTCP:465 -iTCP:2525 -iTCP:25')
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        output = out.decode()
        time += 1
        if "ESTABLISHED" in output:
            output = output.split(" ")
            # delete empty array elements
            my_list = list(filter(None, output))
            # full ip address with port number
            port_num = my_list[-2]
            # split at the ':' to get port number at last index of array
            get_port = port_num.split(":")
            port = get_port[-1]
            process_name = my_list[8]
            process_n = process_name.split("\n")
            process_name = process_n[-1]
            pid = my_list[9]
            p = psutil.Process(int(pid))
            if process_name not in white_list:
                #GUI/UI 
                title='KEYLOGGER DETECTED!'
                msg= f'Security breach Found \nApplication name: {process_name} \nProcess ID (PID): {pid}\nTrying to communicate on port {port}\n Go_back to Terminal to Black_list or white_list the Process.'
                easygui.msgbox(msg,title)
                print(Fore.CYAN+"KEYLOGGER DETECTED!")
                # terminate process if it exists in blacklist
                if process_name in black_list:
                    p.kill()
                    print(Fore.LIGHTYELLOW_EX+'Blacklist application found running.\nProcess automatically terminated.')
                    time = 1
                # if process is not in whitelist, check if it should be
                elif process_name not in white_list:
                    print(Fore.LIGHTYELLOW_EX+'Pausing application...\n')
                    p.suspend()
                    print(Fore.RED+'Information on application identified in your system to be potential threat...')
                    print(Fore.LIGHTYELLOW_EX+f'Application name: {process_name}\n'
                          f'Process ID (PID): {pid}\n'
                          f'Trying to communicate on port {port}\n')
                    selected = False
                    while not selected:
                        is_safe = input(Fore.LIGHTBLUE_EX+"Would you like to whitelist this application? (Y/N): ").lower()
                        if is_safe == 'y':
                            print(Fore.CYAN+"Resuming process...")
                            p.resume()
                            print(Fore.CYAN+"Adding to whitelist...")
                            white_list.append(process_name)
                            selected = True
                            time = 1
                        elif is_safe == 'n':
                            print(Fore.CYAN+"Terminating process...")
                            p.kill()
                            print(Fore.BLUE+"Adding to blacklist...")
                            black_list.append(process_name)
                            selected = True
                            time = 1

                        print(Fore.WHITE+Fore.BLUE+'whitelist:', white_list)
                        print(Fore.WHITE+Fore.RED+'blacklist:', black_list)