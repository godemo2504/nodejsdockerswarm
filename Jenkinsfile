pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "godemo2504/simple-node-swarm"
    IMAGE_TAG = ""
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
          sh 'pwd && ls -la'
          def imageTagLocal = sh(script: "git rev-parse --short=7 HEAD", returnStdout: true).trim()
          echo "imageTagLocal = '${imageTagLocal}'"
          if (imageTagLocal == null || imageTagLocal == '') {
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
          sh "docker build -t ${DOCKERHUB_REPO}:$IMAGE_TAG ."
        }
      }
    }

    stage('Login DockerHub & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push ${DOCKERHUB_REPO}:$IMAGE_TAG
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withCredentials([string(credentialsId: 'kubeconfig-credentials-id', variable: 'KUBECONFIG_CONTENT')]) {
          sh '''
            echo "$KUBECONFIG_CONTENT" > kubeconfig_tmp
            export KUBECONFIG=$(pwd)/kubeconfig_tmp
            envsubst < app/k8s/deployment.yml | kubectl apply -f -
          '''
        }
      }
    }
  }
}
