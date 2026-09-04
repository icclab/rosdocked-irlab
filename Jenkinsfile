pipeline {
  agent any
  
  environment {
    DOCKERHUB_CREDENTIALS=credentials('dockerhub-robopaas')
  	}
   
  stages {
    stage('Run Builds') {
	parallel {
		stage('Build on  CPU') {
			steps {
				sh "chmod +x -R ${env.WORKSPACE}"
				//echo 'Building BASE_CPU image...'
				//sh "cd ./BASE_CPU/  && ./build.sh"
				echo 'Building BASE_CPU_with_workspace image...'
         			sh "cd ./WORKSPACE/  && ./build_cpu_with_workspace.sh"
			}
			post {        
				failure {
          				echo "Build CPU failed"
       				}
      	   		}
		}
		stage('Build on K8s') {
			steps {
				sh "chmod +x -R ${env.WORKSPACE}"
				//echo 'Building BASE_K8S image...'
				//sh "cd ./BASE_K8S/  && ./build.sh"
				echo 'Building BASE_K8S_with_workspace image...'
         			sh "cd ./WORKSPACE/  && ./build_k8s_with_workspace.sh"
			}
			post {        
				failure {
          				echo "Build K8S failed"
       				}
      	   		}
		}
	}
    }	

  stage('Run Tests') {
	 parallel {
		stage('Testing on CPU') {
			steps {
				echo 'Testing grasping stack... '
	 			sh "cd ./test/ && ./run_grasp_test_bash_cpu.sh"
				//echo 'Testing navigation stack... '
	 			//sh "cd ./test/ && ./run_nav_test_bash_cpu.sh"
			}
			post {        
				failure {
          				echo "Testing on CPU failed"
       				}
      	   		}
		} 
		stage('Testing on K8S') {
			steps {
				echo 'Testing grasping stack... '
	 			sh "cd ./test/ && ./run_grasp_test_bash_k8s.sh"
				//echo 'Testing navigation stack... '
	 			//sh "cd ./test/ && ./run_nav_test_bash_k8s.sh"
			}
			post {        
				failure {
          				echo "Testing on K8s failed"
       				}
      	   		}
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
				// Push exactly the images the build stages above produced. These
				// names come from images.env, the same file the build scripts use,
				// so CI can no longer publish a different set than it built (it
				// used to build jazzy and push noetic).
				sh '''
				  . ./images.env
				  for img in "$CPU_IMAGE" "$K8S_IMAGE"; do
				    docker push "$img"
				    # Also publish an immutable build-numbered tag for rollbacks.
				    docker image tag "$img" "${img%:*}:jenkins-${BUILD_NUMBER}"
				    docker push "${img%:*}:jenkins-${BUILD_NUMBER}"
				  done
				'''
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


