pipeline {
  agent any

  environment {
    DOCKER_BUILDKIT = "1"
  }

  stages {
    stage('Clone Repo') {
      steps {
        git 'https://github.com/Praven4754/Attendance-Assistant-Phidata.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t attendance-assistant .'
      }
    }

    stage('Create ConfigMap (env)') {
      steps {
        sh '''
          echo "[INFO] Recreating Kubernetes ConfigMap..."
          kubectl delete configmap attendance-env --ignore-not-found
          kubectl create configmap attendance-env --from-env-file=/env/.env
        '''
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        sh 'kubectl apply -f deployment.yaml'
      }
    }
  }
}
