pipeline {
  agent any
  
  environment {
    DOCKERHUB_CREDENTIALS=credentials('dockerhub-robopaas')
  	}
   
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
          echo 'Testing navigation stack...'
	  sh "docker image ls"  
	  sh "docker run -ti --name test_container robopaas/rosdocked-noetic-cpu:latest "
	  sh 'docker ps'
	  sh 'docker exec test_container "caktin build; roslaunch /home/ros/catkin_ws/src/icclab_summit_xl/launch/irlab_sim_summit_xls_grasping.launch" '
	    
          sh "docker run robopaas/rosdocked-noetic-cpu:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/nav_test_bash.sh"
          sh "docker run robopaas/rosdocked-noetic-gpu:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/nav_test_bash.sh"
          sh "docker run robopaas/rosdocked-noetic-k8s:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/nav_test_bash.sh"
	 
	  echo 'Testing grasping stack...'
          sh "docker run robopaas/rosdocked-noetic-cpu:latest roslaunch /home/ros/catkin_ws/src/icclab_summit_xl/launch/irlab_sim_summit_xls_grasping.launch"
          sh "docker run robopaas/rosdocked-noetic-gpu:latest roslaunch /home/ros/catkin_ws/src/icclab_summit_xl/launch/irlab_sim_summit_xls_grasping.launch"
          sh "docker run robopaas/rosdocked-noetic-k8s:latest roslaunch /home/ros/catkin_ws/src/icclab_summit_xl/launch/irlab_sim_summit_xls_grasping.launch"	      
      }
      post{
        failure {
          echo "Test failed" 
       		}
      	  }
   	}
    
     stage('Login') {
			steps {
				sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
			}
      post {
        failure {
          echo "Login failed" 
        	}
	  }
       }
	
	stage('Push') {
			steps {
				sh 'docker push robopaas/rosdocked-noetic-base-cpu:latest'
				sh 'docker push robopaas/rosdocked-noetic-base-gpu:latest'
				sh 'docker push robopaas/rosdocked-noetic-base-k8s:latest'
				sh 'docker push robopaas/rosdocked-noetic-cpu:latest'
        			sh 'docker push robopaas/rosdocked-noetic-gpu:latest'
        			sh 'docker push robopaas/rosdocked-noetic-k8s:latest'
				}
     			 post {
      				  failure {
       					   echo "Image push failed" 
     					   }
				}
			}
 	 }
	
	post {
		always {
			sh 'docker logout'
		}
	}

}


