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
                bat '''
                    docker run --rm %IMAGE_NAME% python -c "from app import app; print('App imported successfully')"
                '''
            }
        }

        stage('Dependency Check (OWASP)') {
            steps {
                echo '>>> Running OWASP Dependency Check...'
                dependencyCheck additionalArguments: '''
                    --scan ./backend
                    --format HTML
                    --format XML
                    --out ./dependency-check-report
                ''', odcInstallation: 'OWASP-DC'
            }
            post {
                always {
                    dependencyCheckPublisher pattern: 'dependency-check-report/dependency-check-report.xml'
                }
            }
        }

        stage('Security Scan') {
            steps {
                echo '>>> Running security vulnerability scan...'
                bat '''
                    docker run --rm %IMAGE_NAME% pip install safety
                    docker run --rm %IMAGE_NAME% safety check
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '>>> Deploying container...'
                bat '''
                    docker stop %CONTAINER_NAME% || exit 0
                    docker rm %CONTAINER_NAME%   || exit 0
                    docker run -d --name %CONTAINER_NAME% -p 5000:5000 %IMAGE_NAME%
                '''
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