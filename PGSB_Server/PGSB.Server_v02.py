#!/usr/bin/env python3

"""
Python Game Server Backup
PGSB.Server_v02.py
Author: user / Stefan Czopak
Date: 6. August 2023
Description: The Server sided script for automatically backing up a speciefed server directory. 
A subprocess will be seachred by name an terminated and server gets started again after all files are copied.
You can add this script to Cron task scheduler.
"""

import time, os, signal, psutil, shutil, datetime, subprocess

#start path for the game server
bashCommand="/home/user/path/to/gameserver/start.sh"

#name of servers process - this will be searched and terminated as subprocess  
process_name= "java"

#jar path
jar_path = "/home/user/minecraftManu"

#path to the Backup location
date=str(datetime.datetime.now().date())
backup_path="/home/user/backup/path/" + date

#path to the Server location
server_path="/home/user/serverlocation"

# set path to java
java_command = "/usr/bin/java"

# Set the JAVA_HOME environment variable
java_home_path = "/usr/lib/jvm/java-17-openjdk-amd64"
os.environ['JAVA_HOME'] = java_home_path

#get process PID by name
def get_pid(process_name):
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return proc.pid
        
def checkProcessState():
    if(get_pid(process_name) != None):
        return True
    else: 
        print("The Process '" + process_name + "' could not be found. Or the returned value is null")
        return False
       
#kill process by PID with refrence check
def kill_pid():
    if(checkProcessState() is True):
        os.kill(get_pid(process_name),signal.SIGINT)
        time.sleep(10)
    else:
        return False

def start_server_with_bash():
    sleep_counter = 0
    if(checkProcessState() is False):
        with open('subprocess_output.txt', 'w') as output_file:
            subprocess.Popen([java_command, '-Xms5G', '-Xmx5G', '-XX:+UseG1GC', '-jar', 'paper-1.19.2-307.jar', '--nogui'],
                stdout=output_file, stderr=subprocess.STDOUT, cwd=jar_path)
        #os.system(bashCommand)
        while checkProcessState() is False:
            sleep_counter = sleep_counter + 1
            print("Sleep Counter runs")
            time.sleep(10)
        print("Server is started")
        return True;

#backup the files from the path's specified above
def backup_files():
    if(checkProcessState() is False):
        shutil.copytree(server_path, backup_path, symlinks=False, ignore=None)
        #os.rename(backup_path + "/minecraftManu", datetime.date + "-" + datetime.time)
        return True

def initialize():
    if(kill_pid() is False):
        print("No Process terminated")
    if(backup_files() != True):
        print("Backing up Files failed")
    if(start_server_with_bash() != True):
        print("Server could not be startet")


initialize()