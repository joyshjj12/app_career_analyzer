pipeline {
    agent any
    
    // Define environment variables
    environment {
        // *** This is the updated line ***
        DOCKER_IMAGE = "joyshjj1234/resume-analyzer"  
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"
       
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Code pulled from Git.'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build image: joyshjj12/resume-analyzer:build-1, build-2, etc.
                    sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ./app"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                // Ensure you have a Jenkins credential with ID 'docker-hub-creds'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USER')]) {
                    // Logs into Docker Hub using credentials stored in Jenkins
                    sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD}"
                    sh "docker push ${DOCKER_IMAGE}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "sed -i 's|:latest|:${IMAGE_TAG}|g' k8s/deployment.yaml" 
                
                // CRITICAL FINAL FIX: Use a temporary file to bypass Windows permission bug
                sh """
                # 1. Read the config content and write it to a temporary, local file
                #    The 'cp' or 'echo' method is often more reliable on Windows mounts.
                cp /root/.kube/config kubeconfig_temp
                
                # 2. Use the temporary file (owned by jenkins) for kubectl
                kubectl --kubeconfig kubeconfig_temp apply -f k8s/deployment.yaml
                kubectl --kubeconfig kubeconfig_temp apply -f k8s/service.yaml
                
                # 3. Clean up the temporary file
                rm kubeconfig_temp
                """
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f'
        }
    }
}