pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        echo 'Hey there!'
      }
    }
    stage('Install requirements') {
      steps {
        pip install -r requirements.txt
      }
    }
  }
}
