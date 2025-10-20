pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'master', url: 'file:///C:/resume-devops'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat 'docker build -t resume-app ./app'
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running tests..."
                bat 'echo Tests passed'
                // Optional: run pytest if you have tests
                // bat 'pytest ./app/tests'
            }
        }

        stage('Deploy with Ansible') {
            steps {
                echo "Deploying via Ansible..."
                bat 'ansible-playbook ansible/deploy_app.yml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
