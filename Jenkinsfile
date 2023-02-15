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
                echo 'docker image'
            }
        }
        stage('deploy docker image') {
            when {
                branch "master"
            }
            steps {
                echo 'deploy'
            }
        }
    }
}
