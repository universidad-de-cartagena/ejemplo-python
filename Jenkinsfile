pipeline {
  agent {
    label 'equipo01'
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub-account')
  }
  stages {
    stage('Build image') {
      post {
        success {
          echo '====++++A executed succesfully++++===='
          sh "docker login --username ${DOCKERHUB_CREDENTIALS_USR} --password ${DOCKERHUB_CREDENTIALS_PSW}"
          sh 'docker tag ejemplo-python:latest equipo01-backend:latest'
          sh 'docker push equipo01-backend:latest'
        }
        failure {
          echo '====++++A execution failed++++===='
          sh 'docker container prune -f'
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
          echo 'docker-compose -f docker-compose.prod-yml down -v -t 0 --remove-orphans --rmi all'
        }
      }
      steps {
        sh 'docker-compose -f docker-compose.prod-yml up -d'
      }
    }
  }
}
