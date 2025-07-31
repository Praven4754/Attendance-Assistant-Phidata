pipeline {
    agent { label 'jenkins' }

    environment {
        IMAGE_NAME = "pravenkumar871/attendance-assistant"
        CONTAINER_NAME = "attendance-assistant"
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
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                        '''
                    }
                }
            }
        }

        stage('Run Application Container') {
            steps {
                script {
                    sh '''
                        docker rm -f ${CONTAINER_NAME} || true
                        docker run -d --name ${CONTAINER_NAME} -p 7860:7860 \
                        -v /vagrant/jenkins/.env:/app/.env \
                        ${IMAGE_NAME}:${BUILD_NUMBER}
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment succeeded."
        }
        failure {
            echo "❌ Deployment failed."
        }
    }
}
