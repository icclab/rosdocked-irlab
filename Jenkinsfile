pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
          echo 'Building...'
          sh './BASE_CPU/build.sh'
      }
      post{
        failure {
          echo "Build failed"
        }
      }
    }

    stage('Test') {
      steps {
          echo 'Testing...'
      }
    }
  
    stage('Deploy') {
      steps {
          echo 'Deploying...'
      }
    }
  }
}


