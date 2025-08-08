pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "godemo2504/simple-node-swarm"
    SSH_USER = "root"
    SSH_HOST = "161.35.222.219"
    DEPLOY_DIR = "/root/deploy"
  }

  stages {
    stage('Checkout') {
      steps {
        // On récupère le code et la config git
        checkout scm
      }
    }

    stage('Prepare variables') {
      steps {
        script {
          // Récupérer le hash git court de la version checkoutée
          def gitCommitShort = sh(script: 'git rev-parse --short=7 HEAD', returnStdout: true).trim()
          env.IMAGE_TAG = "${env.BUILD_NUMBER}-${gitCommitShort}"
          echo "IMAGE_TAG = ${env.IMAGE_TAG}"
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        dir('app') {
          sh "docker build -t ${DOCKERHUB_REPO}:${env.IMAGE_TAG} ."
        }
      }
    }

    stage('Login DockerHub & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh "echo $DH_PASS | docker login -u $DH_USER --password-stdin"
          sh "docker push ${DOCKERHUB_REPO}:${env.IMAGE_TAG}"
        }
      }
    }

    stage('Deploy to Swarm master') {
      steps {
        sshagent(credentials: ['swarm-master-ssh']) {
          sh "scp docker/docker-stack.yml ${SSH_USER}@${SSH_HOST}:/tmp/docker-stack.yml"
          sh """
            ssh ${SSH_USER}@${SSH_HOST} \\
              "export DOCKERHUB_REPO=${DOCKERHUB_REPO} TAG=${env.IMAGE_TAG} && \\
               docker stack deploy -c /tmp/docker-stack.yml nodeapp_stack"
          """
        }
      }
    }
  }

  post {
    success {
      echo "Déploiement terminé: ${DOCKERHUB_REPO}:${env.IMAGE_TAG}"
    }
    failure {
      echo "Pipeline échouée"
    }
  }
}
