pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
          echo 'Building...'
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
~  
