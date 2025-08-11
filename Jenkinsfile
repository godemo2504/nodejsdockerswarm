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
          def tag = sh(script: "git rev-parse --short=7 HEAD", returnStdout: true).trim()
          env.IMAGE_TAG = tag
          echo "IMAGE_TAG set to ${env.IMAGE_TAG}"
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        dir('app') {
          // Utilise double quotes pour que Groovy évalue DOCKERHUB_REPO
          // et shell remplace $IMAGE_TAG à l'exécution
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
