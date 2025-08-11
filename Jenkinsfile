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
          sh "docker build -t ${env.DOCKERHUB_REPO}:${env.IMAGE_TAG} ."
        }
      }
    }

    stage('Login DockerHub & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          // Attention ici on ne peut pas éviter le warning 100% à cause de echo "$DH_PASS" mais c'est safe car c'est la seule façon docker login accepte le pass
          sh '''
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push ${DOCKERHUB_REPO}:${IMAGE_TAG}
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig-credentials-id', variable: 'KUBECONFIG_FILE')]) {
          sh '''
            export KUBECONFIG=$KUBECONFIG_FILE
            envsubst < app/k8s/deployment.yml | kubectl apply -f -
          '''
        }
      }
    }
  }
}
