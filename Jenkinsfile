pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:24.0.7-cli
    command:
    - cat
    tty: true
  - name: kubectl
    image: bitnami/kubectl:latest
    command:
    - cat
    tty: true
  - name: python
    image: python:3.10
    command:
    - cat
    tty: true
"""
    }
  }

  environment {
    DOCKER_BUILDKIT = 1
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        container('docker') {
          sh 'docker build -t attendance-assistant .'
        }
      }
    }

    stage('Push to Local Registry or Docker Hub') {
      steps {
        container('docker') {
          // Example: `docker tag` + push to your preferred registry
          echo 'Push step skipped (you can customize)'
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        container('kubectl') {
          sh '''
          kubectl delete deployment attendance-assistant --ignore-not-found
          kubectl create deployment attendance-assistant --image=attendance-assistant
          kubectl expose deployment attendance-assistant --type=NodePort --port=7860
          '''
        }
      }
    }
  }
}
