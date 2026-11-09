pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'hibahtaj/december:latest'
    }
    stages {
        stage('Run Selenium Tests') {
            steps {
                echo 'Running Selenium Tests'
                sh '''
                    python3 -m pip install -r requirements.txt
                    python3 app.py > flask.log 2>&1 &
                    APP_PID=$!
                    trap 'kill $APP_PID 2>/dev/null || true' EXIT
                    python3 -m pytest tests/ -v
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Build Docker Image'
                sh 'docker build -t testimg.'
            }
        }
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'echo "$DOCKER_PASSWORD" | docker login -u "hibahtaj" --password-stdin'
                }
            }
        }
        stage('Push Docker Image to Docker Hub') {
            steps {
                echo 'Push Docker Image to Docker Hub'
                sh 'docker push testimg'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    sed "s|hibahtaj/exam:latest|testimg|g" kubernetes/deployment.yaml | kubectl apply -f -
                    kubectl apply -f kubernetes/service.yaml
                    kubectl rollout status deployment/december-deployment --timeout=120s
                '''
            }
        }
    }
    post {
        success { echo 'Pipeline successful' }
        failure { echo 'Pipeline failed' }
    }
}
