"""
Python Game Server Backup
PGSB.Client_v02.py
Author: PapaFringo / Stefan Czopak
Date: 6. August 2023
Description: The Client sided script for automatically Downloading the most rescent Directory on a specified path.
You can add this script to Task Scheduler.
"""


import ftplib
import os

#The source directory on the server
src_dir = "/path/to/source/dir/"

#The destination on you machine
dest_dir = "./Backups/"


def ftp_connect(host, user, passw):
    FTP = ftplib.FTP(host)
    try:
        print("Connect to FTP...")
        print(FTP.login(user, passw))
        return FTP
    except ConnectionError as e:
        print(f"Error: {e}")


def get_latest_folder(FTP, src_dir):
    ordner_list = []
    FTP.cwd(src_dir)
    FTP.retrlines('LIST', ordner_list.append)
    ordner_list.sort()

    if len(ordner_list) <= 0:
        print("Dir Empty")
    else:
        last_entry = str(ordner_list[-1])
        substring = last_entry[56:83]
        print(f"The Folder: '{substring}' will be copied!")
        return src_dir + "/" + substring


def download_folder(ftp: ftplib.FTP, src_path, dest_path):
    try:
        
        ftp.cwd(src_path)
    except Exception as e:
        print(f"Error on trying to change Directory: {e}")
        print(f"src_path: {src_path}")
        return False

    try:
       
        os.makedirs(dest_path, exist_ok=True)
        files = ftp.nlst()

        for file in files:
            local_path = os.path.join(dest_path, file)

            try:
                ftp.cwd(file)
                download_folder(ftp, src_path + "/" + file, local_path)
                ftp.cwd('..')
            except ftplib.error_perm:
                with open(local_path, 'wb') as f:
                    print(src_path + "/" + file)
                    ftp.retrbinary('RETR ' + file, f.write)
    except Exception as e:
        print(f"Error while Downloading Directory: {e}")
        print(f"src_path: {src_path}")
        print(f"dest_path: {dest_path}")
        return False


if __name__ == "__main__":
    host = "hostIP"
    user = "user"
    passw = "password"
    ftp = ftp_connect(host, user, passw)
    src_path = get_latest_folder(ftp, src_dir)
    if src_path:
        download_folder(ftp, src_path, dest_dir)
