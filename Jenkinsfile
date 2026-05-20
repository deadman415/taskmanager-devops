pipeline {
    agent any

    environment {
        IMAGE_NAME = "taskmanager-backend"
        CONTAINER_NAME = "taskmanager-backend"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '>>> Pulling code from GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '>>> Building Docker image...'
                bat 'docker build -t %IMAGE_NAME% ./backend'
            }
        }

        stage('Run Tests') {
            steps {
                echo '>>> Running basic health check...'
                bat 'docker run --rm %IMAGE_NAME% python -c "from app import app; print(\'App imported successfully\')"'
            }
        }

        stage('Dependency Check') {
            steps {
                echo '>>> Checking for outdated dependencies...'
                bat 'docker run --rm %IMAGE_NAME% pip list --outdated'
            }
        }

        stage('Security Scan') {
            steps {
                echo '>>> Running security vulnerability scan...'
                bat 'docker run --rm %IMAGE_NAME% sh -c "pip install pip-audit -q && pip-audit" || echo "Scan complete - review output above"'
            }
        }

        stage('Deploy') {
            steps {
                echo '>>> Deploying container...'
                bat 'docker stop %CONTAINER_NAME% || exit 0'
                bat 'docker rm %CONTAINER_NAME% || exit 0'
                bat 'docker run -d --name %CONTAINER_NAME% -p 5000:5000 %IMAGE_NAME%'
            }
        }

    }

    post {
        success {
            echo '>>> Pipeline completed successfully! App is running.'
        }
        failure {
            echo '>>> Pipeline failed. Check logs above.'
        }
    }
}