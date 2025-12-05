
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Charger les serveurs depuis un fichier
def load_servers(filename="servers.txt"):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Erreur : fichier {filename} introuvable.")
        exit(1)

servers = load_servers()

def ssh_cmd(server, cmd):
    print(f"[+] Connexion à {server} ...")
    result = subprocess.run(["ssh", server, cmd],
                            capture_output=True,
                            text=True)
    return f"--- {server} ---\n{result.stdout or result.stderr}"

def menu():
    print("\n=== MENU SSH PARALLÈLE ===")
    print("1 - hostname")
    print("2 - uptime")
    print("3 - df -h")
    print("4 - free -m")
    print("5 - top -b -n1")
    print("6 - Commande personnalisée")
    print("0 - Quitter")
    return input("Votre choix : ")

def ask_threads():
    try:
        nb = int(input("Nombre de connexions en parallèle (ex: 5) : "))
        return max(1, nb)
    except:
        return 5

while True:
    choix = menu()

    if choix == "0":
        print("Au revoir !")
        break
    elif choix == "1":
        cmd = "hostname"
    elif choix == "2":
        cmd = "uptime"
    elif choix == "3":
        cmd = "df -h"
    elif choix == "4":
        cmd = "free -m"
    elif choix == "5":
        cmd = "top -b -n1"
    elif choix == "6":
        cmd = input("Entrez votre commande : ")
    else:
        print("Choix invalide")
        continue

    threads = ask_threads()

    print("\nExécution en parallèle...\n")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(lambda s: ssh_cmd(s, cmd), servers)

    print("\n========= RÉSULTATS =========\n")
    for r in results:
        print(r)
