pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        echo 'Hey there!'
      }
    }
    stage('Install Python requirements') {
      steps {
        pip install -r requirements.txt
      }
    }
  }
}
