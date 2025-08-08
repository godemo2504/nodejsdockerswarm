pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "godemo2504/simple-node-swarm"
    SSH_USER = "root"
    SSH_HOST = "161.35.222.219"
    DEPLOY_DIR = "/root/deploy"
    IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.com/godemo2504/nodejsdockerswarm.git']]])
      }
    }

    stage('Build Docker Image') {
      steps {
        dir('app') {
          sh "docker build -t ${DOCKERHUB_REPO}:${IMAGE_TAG} ."
        }
      }
    }

    stage('Login DockerHub & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh "echo $DH_PASS | docker login -u $DH_USER --password-stdin"
          sh "docker push ${DOCKERHUB_REPO}:${IMAGE_TAG}"
        }
      }
    }

    stage('Deploy to Swarm master') {
      steps {
        sshagent(credentials: ['swarm-master-ssh']) {
          // Copier le fichier docker-stack.yml sur le serveur distant
          sh "scp docker/docker-stack.yml ${SSH_USER}@${SSH_HOST}:/tmp/docker-stack.yml"

          // Déployer la stack en exportant les variables nécessaires
          sh """
            ssh ${SSH_USER}@${SSH_HOST} \\
              "export DOCKERHUB_REPO=${DOCKERHUB_REPO} TAG=${IMAGE_TAG} && \\
               docker stack deploy -c /tmp/docker-stack.yml nodeapp_stack"
          """
        }
      }
    }
  }

  post {
    success {
      echo "Déploiement terminé: ${DOCKERHUB_REPO}:${IMAGE_TAG}"
    }
    failure {
      echo "Pipeline échouée"
    }
  }
}

