pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
          sh "chmod +x -R ${env.WORKSPACE}"
          echo 'Building BASE_CPU image...'
          sh "pwd"
          sh "cd ./BASE_CPU/ && pwd && ./build.sh"
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


