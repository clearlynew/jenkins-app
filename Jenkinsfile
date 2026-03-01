pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "library-backend"
        FRONTEND_IMAGE = "library-frontend"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                sh 'docker build -t $BACKEND_IMAGE -f dockerfuel/Dockerfile.backend ./backend'
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh 'docker build -t $FRONTEND_IMAGE -f dockerfuel/Dockerfile.frontend ./frontend'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                docker-compose down || true
                docker-compose up -d
                '''
            }
        }
    }

    post {
        success {
            echo "Application deployed successfully."
        }
        failure {
            echo "Pipeline failed. Check console output."
        }
    }
}