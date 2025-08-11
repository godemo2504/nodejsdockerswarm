pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "godemo2504/simple-node-swarm"
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
          def imageTagLocal = sh(script: "git rev-parse --short=7 HEAD", returnStdout: true).trim()
          echo "imageTagLocal = '${imageTagLocal}'"
          if (!imageTagLocal) {
            error("Impossible de récupérer le commit git pour IMAGE_TAG")
          }
          env.IMAGE_TAG = imageTagLocal
          echo "IMAGE_TAG set to ${env.IMAGE_TAG}"
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        dir('app') {
          sh(script: "docker build -t ${DOCKERHUB_REPO}:${env.IMAGE_TAG} .")
        }
      }
    }

    stage('Login DockerHub & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh(script: '''
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push ${DOCKERHUB_REPO}:${IMAGE_TAG}
          ''', env: [ "IMAGE_TAG=${env.IMAGE_TAG}", "DOCKERHUB_REPO=${env.DOCKERHUB_REPO}" ])
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig-credentials-id', variable: 'KUBECONFIG_FILE')]) {
          sh(script: '''
            export KUBECONFIG=$KUBECONFIG_FILE
            envsubst < app/k8s/deployment.yml | kubectl apply -f -
          ''')
        }
      }
    }
  }
}
