import requests
import time
import sys

def check():
    response = requests.get("https://github.com/TyBundy/2D-Platformer/blob/main/version.txt")

    current_version = open("version.txt").read().split(".")
    recent_version = response.json()["payload"]["blob"]["rawLines"][0].split(".")

    new = False

    if int(recent_version[0]) > int(current_version[0]):
        print("A new major version is available, it's very recommended to download this version before continuing to play, as you may miss out on some serious content.")
        new = True

    elif int(recent_version[1]) > int(current_version[1]):
        print("A new minor version is available, it's recommended to download this version as it likely contains some decent content and will enhance your experience.")
        new = True

    elif int(recent_version[2]) > int(current_version[2]):
        print("A new patch is available, it's recommended to download this patch as it likely contains bugfixes which will make your experience more pleasant.")
        time.sleep(2)

    if new:
        x = input("Would you like to continue startup? [y/n]\n>> ").lower()
        if x == "y" or x == "yes" or x == "yes please":
            pass
        if x == "n" or x == "no":
            sys.exit()