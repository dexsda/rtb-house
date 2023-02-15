pipeline {
    agent any
    stages {
        stage('flake8 analysis') {
            steps {
                sh 'flake8 service/service.py'
            }
        }
        stage('build docker image') {
            when {
                branch "master"
            }
            steps {
                sh 'docker-compose -f docker/docker-compose.yml build'
            }
        }
        stage('deploy docker image') {
            when {
                branch "master"
            }
            steps {
                sh 'docker-compose -f docker/docker-compose.yml down -v'
                sh 'docker-compose -f docker/docker-compose.yml up -d --force-recreate'
            }
        }
    }
}
