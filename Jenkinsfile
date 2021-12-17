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
          sh "cd ./BASE_GPU/ && pwd && ./build.sh"
          echo 'Building BASE_K8S image...'
          sh "cd ./BASE_K8S/ && pwd && ./build.sh"
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


