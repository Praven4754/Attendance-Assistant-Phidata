pipeline {
  agent any

  environment {
    IMAGE_NAME = 'praven4754/attendance-assistant'
    TAG = 'latest'
  }

  stages {
    stage('Clone Repo') {
    steps {
        git url: 'https://github.com/Praven4754/Attendance-Assistant-Phidata.git', branch: 'main'
    }
}


    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $IMAGE_NAME:$TAG .'
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push $IMAGE_NAME:$TAG
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        sh '''
          # Step 1: Create or update ConfigMap
          kubectl create configmap attendance-assistant-config --from-env-file=/vagrant/jenkins/.env --dry-run=client -o yaml | kubectl apply -f -

          # Step 2: Apply deployment and service YAMLs
          kubectl apply -f k8s/deployment.yaml
          kubectl apply -f k8s/service.yaml
        '''
      }
    }
  }
}
