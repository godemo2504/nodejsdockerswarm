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
          if (imageTagLocal == null || imageTagLocal == '') {
            error("Impossible de récupérer le commit git pour IMAGE_TAG")
          }
          // stocke dans une variable locale Groovy (pas env)
          env.IMAGE_TAG = imageTagLocal  // utile si tu veux garder en env aussi
          // mais privilégie la variable locale
          script {
            // pour partage entre stages
            IMAGE_TAG = imageTagLocal
          }
          echo "IMAGE_TAG set to ${IMAGE_TAG}"
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        dir('app') {
          script {
            sh "docker build -t ${DOCKERHUB_REPO}:${IMAGE_TAG} ."
          }
        }
      }
    }

    stage('Login DockerHub & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          script {
            sh """
              echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
              docker push ${DOCKERHUB_REPO}:${IMAGE_TAG}
            """
          }
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig-credentials-id', variable: 'KUBECONFIG_FILE')]) {
          script {
            sh """
              export KUBECONFIG=${KUBECONFIG_FILE}
              envsubst < app/k8s/deployment.yml | kubectl apply -f -
            """
          }
        }
      }
    }
  }
}
