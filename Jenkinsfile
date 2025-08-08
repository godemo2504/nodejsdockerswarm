pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "yourdockerhubuser/simple-node-swarm"  // <-- remplacer
    SSH_USER = "root"
    SSH_HOST = "swarm-master.example.com"                   // <-- remplacer
    DEPLOY_DIR = "/root/deploy"
    IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Install & Test') {
      steps {
        dir('app') {
          sh 'npm install --no-audit --no-fund'
          sh 'npm test || true'
        }
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

    stage('Archive Artifact') {
      steps {
        archiveArtifacts artifacts: 'app/**', allowEmptyArchive: false
      }
    }

    stage('Copy source to Swarm master (/root/deploy)') {
      steps {
        sshagent(credentials: ['swarm-master-ssh']) {
          sh "scp -r app ${SSH_USER}@${SSH_HOST}:${DEPLOY_DIR}/${IMAGE_TAG}"
          sh "ssh ${SSH_USER}@${SSH_HOST} \"ln -sfn ${DEPLOY_DIR}/${IMAGE_TAG} ${DEPLOY_DIR}/current || true\""
        }
      }
    }

    stage('Update Swarm stack') {
      steps {
        sshagent(credentials: ['swarm-master-ssh']) {
          sh "scp docker/docker-stack.yml ${SSH_USER}@${SSH_HOST}:/tmp/docker-stack.yml"
          sh "ssh ${SSH_USER}@${SSH_HOST} \"export DOCKERHUB_REPO=${DOCKERHUB_REPO} && export TAG=${IMAGE_TAG} && docker stack deploy -c /tmp/docker-stack.yml nodeapp_stack\""
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
