pipeline {
    agent any

    environment {
        IMAGE_NAME = "pravenkumar871/attendance-assistant"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Checkout source from SCM (your repo)
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${IMAGE_NAME}:${env.BUILD_NUMBER}
                        """
                    }
                }
            }
        }

        stage('Run app.py') {
            steps {
                script {
                    sh """
                    docker run --rm -p 7860:7860 -v /envfile/.env:/app/.env ${IMAGE_NAME}:${env.BUILD_NUMBER}
                    """
                }
            }
        }
    }
}
