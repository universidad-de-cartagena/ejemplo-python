pipeline {
  agent {
    label 'equipo01'
  }
  stages {
    stage('Build image') {
      post {
        always {
          echo '====++++always++++===='

        }

        success {
          echo '====++++A executed succesfully++++===='

        }

        failure {
          echo '====++++A execution failed++++===='

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
          image 'python:3.7.3-alpine3.10'
        }

      }
      post {
        always {
          echo 'always'

        }

        success {
          echo 'A executed succesfully'

        }

        failure {
          echo 'A execution failed'

        }

      }
      steps {
        sh 'python -m venv env'
        sh './env/bin/pip3 install --no-cache-dir --upgrade pip'
        sh './env/bin/pip3 install --no-cache-dir -r requirements.txt'
        sh './env/bin/coverage run --source . --ommit env/ manage.py test --no-input || true'
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
  }
}
