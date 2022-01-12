pipeline {
  agent any
  
  environment {
    DOCKERHUB_CREDENTIALS=credentials('dockerhub-robopaas')
  	}
   
  stages {
    stage('Run Builds') {
	parallel {
		stage('Build on CPU') {
	    		agent {
		    		label "cpu"
	    		}
			steps {
				sh "chmod +x -R ${env.WORKSPACE}"
				echo 'Building BASE_CPU image...'
				sh "cd ./BASE_CPU/  && ./build.sh"
			}
			post {        
				failure {
          				echo "Build CPU failed"
       				}
      	   		}
		}
		stage('Build on GPU') {
	    		agent {
		    		label "gpu"
	    		}
			steps {
				sh "chmod +x -R ${env.WORKSPACE}"
				echo 'Building BASE_GPU image...'
				sh "cd ./BASE_GPU/  && ./build.sh"
			}
			post {        
				failure {
          				echo "Build GPU failed"
       				}
      	   		}
		}
	}
    }
				

  
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
	      
	  echo 'Testing grasping stack... '
	  sh "cd ./test/ && ./run_grasp_test_bash_cpu.sh"
	  sh "cd ./test/ && ./run_grasp_test_bash_gpu.sh"
	  sh "cd ./test/ && ./run_grasp_test_bash_k8s.sh"
          // sh "docker run robopaas/rosdocked-noetic-cpu:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/grasp_test_bash.sh" 
	  // sh "docker run robopaas/rosdocked-noetic-gpu:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/grasp_test_bash.sh"
	  // sh "docker run robopaas/rosdocked-noetic-k8s:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/grasp_test_bash.sh"	
	      
          echo 'Testing navigation stack...'	
	  sh "cd ./test/ && ./run_nav_test_bash_cpu.sh"
	  sh "cd ./test/ && ./run_nav_test_bash_gpu.sh"
	  sh "cd ./test/ && ./run_nav_test_bash_k8s.sh"
          // sh "docker run robopaas/rosdocked-noetic-cpu:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/nav_test_bash.sh"
          // sh "docker run robopaas/rosdocked-noetic-gpu:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/nav_test_bash.sh"
          // sh "docker run robopaas/rosdocked-noetic-k8s:latest /home/ros/catkin_ws/src/icclab_summit_xl/.ci/nav_test_bash.sh"
	 
      
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


