import subprocess
from concurrent.futures import ThreadPoolExecutor

servers = ["serveur1", "serveur2", "serveur3"]

def ssh_cmd(server, cmd):
    print(f"[+] Connexion à {server} ...")
    result = subprocess.run(["ssh", server, cmd],
                            capture_output=True,
                            text=True)
    return f"--- {server} ---\n{result.stdout}"

def menu():
    print("=== Menu SSH en parallèle ===")
    print("1 - hostname")
    print("2 - uptime")
    print("3 - df -h")
    print("4 - custom")
    print("0 - quitter")
    return input("Votre choix : ")

while True:
    choix = menu()

    if choix == "0":
        break
    elif choix == "1":
        cmd = "hostname"
    elif choix == "2":
        cmd = "uptime"
    elif choix == "3":
        cmd = "df -h"
    elif choix == "4":
        cmd = input("Entrez votre commande : ")
    else:
        print("Choix invalide")
        continue

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(lambda s: ssh_cmd(s, cmd), servers)

    for r in results:
        print(r)
