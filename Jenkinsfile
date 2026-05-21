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
                bat 'docker run --rm %IMAGE_NAME% pip list --outdated || exit /b 0'
            }
        }

        stage('Security Scan') {
            steps {
                echo '>>> Running security vulnerability scan...'
                bat 'docker run --rm %IMAGE_NAME% sh -c "pip install pip-audit -q && pip-audit" || exit /b 0'
                echo '>>> Security scan complete.'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        bat """
                            set JAVA_HOME=
                            \"${scannerHome}\\bin\\sonar-scanner.bat\" ^
                            -Dsonar.projectKey=taskmanager-backend ^
                            -Dsonar.sources=./backend ^
                            -Dsonar.host.url=http://localhost:9000 ^
                            -Dsonar.token=squ_f67e90bc30a5fcb0fe859614fa43d18f2a098365
                        """
                    }
                }
            }
}

        stage('Deploy') {
            steps {
                echo '>>> Deploying container...'
                bat 'docker stop %CONTAINER_NAME% || exit /b 0'
                bat 'docker rm %CONTAINER_NAME% || exit /b 0'
                bat 'docker run -d --name %CONTAINER_NAME% -p 5000:5000 %IMAGE_NAME%'
            }
        }

    }

    post {
        success {
            echo '>>> Pipeline completed successfully!'
        }
        failure {
            echo '>>> Pipeline failed. Check logs above.'
        }
    }
}