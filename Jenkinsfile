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
        
          echo 'Building BASE_CPU_with_workspace image...'
          sh "cd ./WORKSPACE/  && ./build_cpu_with_workspace.sh"
          echo 'Building BASE_GPU_with_workspace image...'
          sh "cd ./WORKSPACE/  && ./build_gpu_with_workspace.sh"
          echo 'Building BASE_K8S_with_workspace image...'
          sh "cd ./WORKSPACE/  && ./build_k8s_with_workspace.sh"
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
          sh "docker run robopaas/rosdocked-noetic-cpu:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/nav_test_bash.sh"
          sh "docker run robopaas/rosdocked-noetic-gpu:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/nav_test_bash.sh"
          sh "docker run robopaas/rosdocked-noetic-k8s:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/nav_test_bash.sh"
      }
      post{
        failure {
          echo "Test failed" 
        }
      }
    }
  
    stage('Deploy') {
      steps {
          echo 'Deploying...'
          echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
          docker push robopaas/rosdocked-noetic-cpu:latest
      }
    post{
        failure {
          echo "Deploy failed" 
        }
    }
  }
}


