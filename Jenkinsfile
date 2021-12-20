pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
          sh "chmod +x -R ${env.WORKSPACE}"
          echo 'Building BASE_CPU image...'
          sh "cd ./BASE_CPU/  && ./build.sh"
          echo 'Building BASE_GPU image...'
          sh "cd ./BASE_GPU/  && ./build.sh"
          echo 'Building BASE_K8S image...'
          sh "cd ./BASE_K8S/  && ./build.sh"
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
          sh "cd test/ && pwd && ./nav_test_bash.sh"
      }
      post{
        failure {
          echo "Test failed"
        }
    }
  
    stage('Deploy') {
      steps {
          echo 'Deploying...'
      }
    }
  }
}


