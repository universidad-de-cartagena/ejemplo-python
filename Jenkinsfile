pipeline {
  agent {
    label 'equipo01'
  }
  environment {
    DOCKERHUB = credentials('jenkinsudc-dockerhub-account')
  }
  stages {
    stage('Docker huerfanos') {
      steps {
        sh 'docker container rm --force $(docker ps -a --quiet) || true'
        sh 'docker volume prune --force || true'
        sh 'docker image prune -f'
      }
    }
    stage('Build image') {
      // Solucion sencilla para obtener el SHA1 del commit en pipelines
      // https://issues.jenkins-ci.org/browse/JENKINS-44449
      environment {
        GIT_COMMIT_SHORT = sh(
          script: "printf \$(git rev-parse --short ${GIT_COMMIT})",
          returnStdout: true
        )
      }
      steps {
        sh 'docker-compose build --force-rm'
        sh 'env'
      }
      post {
        success {
          // Bug reportado en golang-docker-credential-helpers que no permite
          // autenticar el cliente Docker a un registry cuando se instala el
          // paquete docker-compose en distribuciones basadas en Debian
          sh 'sudo apt-get remove golang-docker-credential-helpers -y -q'
          sh 'docker login --username $DOCKERHUB_USR --password $DOCKERHUB_PSW'
          sh 'sudo apt-get install docker-compose -y -q'
          sh 'docker tag equipo01-backend-python:latest $DOCKERHUB_USR/equipo01-backend-python:latest'
          sh 'docker tag equipo01-backend-python:latest $DOCKERHUB_USR/equipo01-backend-python:$BUILD_NUMBER-$GIT_COMMIT_SHORT'
          sh 'docker push $DOCKERHUB_USR/equipo01-backend-python:latest'
        }
        failure {
          sh 'echo ups'
        }
      }
    }
    stage('Tests') {
      steps {
        sh 'docker-compose -f docker-compose.test.yml run -T --rm -e TEST_UID=$(id -u) -e TEST_GID=$(id -g) backend'
        script {
          publishHTML([
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'reports/htmlcov/',
            reportFiles: 'index.html',
            reportName: 'Coverage report in HTML',
            reportTitles: ''
          ])
        }
        cobertura(coberturaReportFile: 'reports/coverage.xml', conditionalCoverageTargets: '70, 0, 0', lineCoverageTargets: '80, 0, 0', methodCoverageTargets: '80, 0, 0', sourceEncoding: 'ASCII')
        junit(testResults: 'reports/test_results/*.xml', allowEmptyResults: true)
        sh 'rm -rdf reports/'
      }
    }
    stage('Deploy') {
      steps {
        sh 'docker-compose up -d'
      }
      post {
        failure {
          sh 'docker volume prune --force || true'
          sh 'docker container rm --force $(docker ps -a --quiet) || true'
          sh 'docker image prune -f'
        }
      }
    }
  }
}
