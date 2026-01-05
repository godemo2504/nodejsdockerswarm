#!/usr/bin/env python3
import subprocess, os
from concurrent.futures import ThreadPoolExecutor

LOG_FILE = "ssh_parallel.log"

# Couleurs terminal
R = "\033[91m"   # Rouge
G = "\033[92m"   # Vert
Y = "\033[93m"   # Jaune
B = "\033[94m"   # Bleu
W = "\033[0m"    # Reset

# Charger serveurs
def load_servers(filename="servers.txt"):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{R}ERREUR : Fichier {filename} introuvable.{W}")
        exit(1)

servers = load_servers()

# Logging
def log(text):
    with open(LOG_FILE, "a") as f:
        f.write(text + "\n")

# Ping
def ping(server):
    result = subprocess.run(["ping", "-c", "1", "-W", "1", server],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        print(f"{G}[OK] {server} répond au ping{W}")
        return True
    else:
        print(f"{R}[KO] {server} ne répond pas{W}")
        return False

# SSH
def ssh_cmd(server, cmd, user):
    target = f"{user}@{server}" if user else server
    print(f"{B}[SSH] Connexion à {target} ...{W}")

    result = subprocess.run(["ssh", target, cmd],
                            capture_output=True,
                            text=True)

    output = f"\n--- {server} ---\n{result.stdout or result.stderr}\n"
    print(output)
    log(output)
    return output

# Menu
def menu():
    print(f"""
{Y}===== MENU SSH PARALLÈLE ====={W}
1 - hostname
2 - uptime
3 - df -h
4 - free -m
5 - top -b -n1
6 - Commande personnalisée
7 - Exécuter sur un seul serveur
8 - Tester le ping sur tous les serveurs
9 - Afficher les logs
0 - Quitter
""")
    return input("Votre choix : ")

# Nombre de threads
def ask_threads():
    try:
        nb = int(input(f"{Y}Nombre de connexions SSH en parallèle : {W}"))
        return max(1, nb)
    except:
        return 5

# Choix du user
def ask_user():
    u = input("Utilisateur SSH (laisser vide pour user actuel) : ")
    return u.strip()

# Choix serveur unique
def choose_server():
    print(f"{B}Liste des serveurs :{W}")
    for i, s in enumerate(servers):
        print(f"{i+1} - {s}")
    choix = int(input("Choisissez un serveur : "))
    return servers[choix-1]

# Afficher logs
def show_logs():
    if not os.path.exists(LOG_FILE):
        print(f"{R}Aucun log disponible.{W}")
        return
    print(f"{G}\n===== LOGS ====={W}")
    with open(LOG_FILE, "r") as f:
        print(f.read())

# Programme principal
while True:
    choix = menu()

    if choix == "0":
        print(f"{G}Au revoir !{W}")
        break

    if choix == "8":
        print(f"{Y}Test ping en parallèle...{W}")
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(ping, servers)
        continue

    if choix == "9":
        show_logs()
        continue

    if choix == "7":
        server = choose_server()
        cmd = input(f"Commande à exécuter sur {server} : ")
        user = ask_user()
        ssh_cmd(server, cmd, user)
        continue

    # Commandes prédéfinies
    if choix == "1":
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
        cmd = input("Votre commande personnalisée : ")
    else:
        print(f"{R}Choix invalide !{W}")
        continue

    threads = ask_threads()
    user = ask_user()

    print(f"{G}\nExécution en parallèle...\n{W}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(lambda s: ssh_cmd(s, cmd, user), servers)

    print(f"{G}=== Fin d'exécution ==={W}")


repoServer:
  livenessProbe: null
  readinessProbe: null

