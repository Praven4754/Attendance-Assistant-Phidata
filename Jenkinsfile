pipeline {
    agent any

    environment {
        IMAGE_NAME = "pravenkumar871/attendance-assistant"
        KUBE_DEPLOYMENT_NAME = "attendance-assistant"
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Praven4754/Attendance-Assistant-Phidata.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                    kubectl delete deployment ${KUBE_DEPLOYMENT_NAME} --ignore-not-found
                    kubectl create deployment ${KUBE_DEPLOYMENT_NAME} --image=${IMAGE_NAME}:${BUILD_NUMBER}
                    kubectl expose deployment ${KUBE_DEPLOYMENT_NAME} --type=NodePort --port=7860 --target-port=7860 --name=${KUBE_DEPLOYMENT_NAME}-service
                    """
                }
            }
        }
    }
}
