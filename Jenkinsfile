pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "godemo2504/simple-node-swarm"
    SSH_CREDENTIALS_ID = "root"        // ID des credentials SSH dans Jenkins
    SSH_HOST = "161.35.222.219"
    DEPLOY_PATH = "/tmp/docker-stack.yml"
  }

  stages {
    stage('Checkout SCM') {
      steps {
        checkout scm
      }
    }

    stage('Prepare variables') {
      steps {
        script {
          IMAGE_TAG = sh(script: "git rev-parse --short=7 HEAD", returnStdout: true).trim()
          echo "IMAGE_TAG = ${IMAGE_TAG}"
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
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh """
            echo $DH_PASS | docker login -u $DH_USER --password-stdin
            docker push ${DOCKERHUB_REPO}:${IMAGE_TAG}
          """
        }
      }
    }

    stage('Deploy to Swarm master') {
      steps {
        sshagent([SSH_CREDENTIALS_ID]) {
          sh """
            ssh-keyscan -H ${SSH_HOST} >> ~/.ssh/known_hosts
            scp docker/docker-stack.yml root@${SSH_HOST}:${DEPLOY_PATH}
            ssh root@${SSH_HOST} "docker stack deploy -c ${DEPLOY_PATH} simple-node-swarm"
          """
        }
      }
    }
  }

  post {
    failure {
      echo 'Pipeline échouée'
    }
  }
}
