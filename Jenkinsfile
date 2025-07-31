pipeline {
    agent { label 'jenkins' }

    environment {
        IMAGE_NAME = "pravenkumar871/attendance-assistant"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${IMAGE_NAME}:${env.BUILD_NUMBER}"
                    }
                }
            }
        }

        stage('Run Application Container') {
            steps {
                script {
                    sh "docker run --rm -d -p 7860:7860 -v /vagrant/jenkins/.env:/app/.env ${IMAGE_NAME}:${env.BUILD_NUMBER}"
                }
            }
        }
    }
}
