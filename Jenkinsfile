pipeline {
  agent {
    label 'equipo01'
  }
  stages {
    stage('Limpiar elementos Docker huerfanos') {
      steps {
        sh 'docker container prune --force || true'
        sh 'docker volume prune --force || true'
        sh 'docker image prune -f'
      }
    }
    stage('Crear de imagen Docker') {
       steps {
        sh 'docker-compose build --force-rm'
      }
      post {
        failure {
          sh 'docker image prune -f'
        }
      }
    }
    stage('Tests') {
      steps {
        sh 'docker-compose -f docker-compose.test.yml run -T --rm -e TEST_UID=$(id -u) -e TEST_GID=$(id -g) backend'
        junit(testResults: 'reports/test_results/*.xml', allowEmptyResults: true)
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
      }
      post {
        always {
          sh 'rm -rdf reports/'
        }
      }
    }
    stage('Publicar imagen Docker') {
      when {
          branch 'master'
      }
      environment {
        DOCKERHUB = credentials('jenkinsudc-dockerhub-account')
        // Solucion sencilla para obtener el SHA1 del commit en pipelines
        // https://issues.jenkins-ci.org/browse/JENKINS-44449
        GIT_COMMIT_SHORT = sh(
          script: "printf \$(git rev-parse --short ${GIT_COMMIT})",
          returnStdout: true
        )
      }
      steps {
        sh 'docker login --username $DOCKERHUB_USR --password $DOCKERHUB_PSW'
        sh 'sudo apt-get install docker-compose -y -q'
        sh 'docker tag equipo01-backend-python:latest $DOCKERHUB_USR/equipo01-backend-python:latest'
        sh 'docker tag equipo01-backend-python:latest $DOCKERHUB_USR/equipo01-backend-python:$GIT_COMMIT_SHORT'
        sh 'docker push $DOCKERHUB_USR/equipo01-backend-python:latest'
        sh 'docker push $DOCKERHUB_USR/equipo01-backend-python:$GIT_COMMIT_SHORT'
      }
      post {
        failure {
          sh 'docker image prune -f'
        }
      }
    }
    stage('Deploy') {
      when {
          branch 'master'
      }
      steps {
        sh 'docker-compose up -d'
      }
      post {
        failure {
          sh 'docker container prune --force || true'
          sh 'docker volume prune --force || true'
          sh 'docker image prune -f'
        }
      }
    }
  }
}
