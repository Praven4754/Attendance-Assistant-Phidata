pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'pravenkumar871/attendance-assistant:latest'
        DOCKER_CREDS = 'dockerhub-creds'
        ENV_PATH = '/envfile/.env'  // Mounted at runtime
    }

    stages {
        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Copy .env & Build Docker Image') {
            steps {
                sh '''
                    cp ${ENV_PATH} .env
                    docker build -t $DOCKER_IMAGE .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS}", usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/deployment.yaml --kubeconfig=/var/jenkins_home/k8s/kubeconfig-jenkins.yaml --validate=false'
                sh 'kubectl apply -f k8s/service.yaml --kubeconfig=/var/jenkins_home/k8s/kubeconfig-jenkins.yaml'
            }
        }
    }
}
