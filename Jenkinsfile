pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
          sh "chmod +x -R ${env.WORKSPACE}"
          echo 'Building BASE_CPU image...'
          echo "The present working directory is `pwd`"
          sh "cd BASE_CPU"
          sh "./build.sh"
          echo 'Building BASE_GPU image...'
          sh "./BASE_GPU/build.sh"
          echo 'Building BASE_K8S image...'
          sh "./BASE_K8S/build.sh"
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


