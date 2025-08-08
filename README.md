# Projet simple Node.js - Déploiement Docker Swarm

## Prérequis
- GitLab repo
- Jenkins (avec plugins SSH et Credentials)
- Docker sur Jenkins agent (ou agent capable de builder)
- Docker Swarm sur les machines (master & workers)
- Compte Docker Hub
- Clé SSH (Jenkins -> Swarm master)

## Déploiement
1. Push du code sur GitLab
2. GitLab webhook déclenche Jenkins
3. Jenkins build l'image et la push sur Docker Hub
4. Jenkins copie les sources sur /root/deploy/<tag> sur le master
5. Jenkins/Ansible déploie le stack sur Swarm (docker stack deploy)

## Variables à modifier
- `Jenkinsfile` : DOCKERHUB_REPO, SSH_HOST
- `ansible/inventory.ini` : hôtes
- Créer credentials Jenkins : dockerhub-creds, swarm-master-ssh
# nodejsdockerswarm
