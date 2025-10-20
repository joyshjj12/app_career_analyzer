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
                // IMPORTANT: The credentialsId 'minikube-config-file' MUST match the ID 
                // you assigned when uploading the config-portable file to Jenkins.
                withCredentials([file(credentialsId: 'minikube-config-file', variable: 'KUBECONFIG_PATH')]) {
                    
                    // 1. Substitution: Update the image tag in the deployment file
                    sh "sed -i 's|:latest|:${IMAGE_TAG}|g' k8s/deployment.yaml" 
                    
                    // 2. Deployment: Use the securely injected KUBECONFIG_PATH variable
                    // This variable points to the temporary, self-contained file inside the container.
                    sh """
                    kubectl --kubeconfig ${KUBECONFIG_PATH} apply -f k8s/deployment.yaml
                    kubectl --kubeconfig ${KUBECONFIG_PATH} apply -f k8s/service.yaml
                    """
                }
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f'
        }
    }
}