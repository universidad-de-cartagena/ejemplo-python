pipeline {
  agent {
    label 'equipo01'
  }
  environment {
    DOCKERHUB = credentials('jenkinsudc-dockerhub-account')
  }
  stages {
    stage('Kill everything') {
      steps {
        sh 'docker-compose down -v --remove-orphans || true'
      }
    }
    stage('Build image') {
      post {
        success {
          echo '====++++A executed succesfully++++===='
          sh 'docker login --username $DOCKERHUB_USR --password $DOCKERHUB_PSW'
          sh 'docker tag ejemplo-python:latest $DOCKERHUB_USR/equipo01-backend:latest'
          sh 'docker push $DOCKERHUB_USR/equipo01-backend:latest'
        }
        failure {
          echo '====++++A execution failed++++===='
          sh 'docker system prune --volumes --force || true'
        }
      }
      steps {
        sh 'docker build -t ejemplo-python:latest .'
      }
    }
    stage('Tests') {
      agent {
        docker {
          label 'equipo01'
          image 'python:3.7.4-stretch'
        }
      }
      steps {
        sh 'python -m venv env'
        sh './env/bin/pip3 install --no-cache-dir --upgrade pip'
        sh './env/bin/pip3 install --no-cache-dir -r requirements.txt'
        sh "./env/bin/coverage run --source '.' --omit 'env/*' manage.py test --no-input || true"
        sh './env/bin/coverage report --show-missing -m'
        sh './env/bin/coverage html'
        script {
          publishHTML([
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'htmlcov/',
            reportFiles: 'index.html',
            reportName: 'Coverage report in HTML',
            reportTitles: ''
          ])
        }
        sh 'rm -rf htmlcov'
        sh './env/bin/coverage xml'
        cobertura(coberturaReportFile: 'coverage.xml', conditionalCoverageTargets: '70, 0, 0', lineCoverageTargets: '80, 0, 0', methodCoverageTargets: '80, 0, 0', sourceEncoding: 'ASCII')
        sh 'rm .coverage coverage.xml'
        junit(testResults: 'test_results/*.xml', allowEmptyResults: true)
      }
    }
    stage('Deploy') {
      post {
        failure {
          echo 'A execution failed'
          sh 'docker-compose down -v --remove-orphans || true'
          sh 'docker system prune --volumes --force || true'
        }
      }
      steps {
        sh 'docker-compose up -d'
      }
    }
  }
}
