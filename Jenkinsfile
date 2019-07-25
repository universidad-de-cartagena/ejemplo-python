pipeline {
    agent none
// Simple vs Double quotes
// https://stackoverflow.com/questions/37464887/vs-vs-in-groovy-when-to-use-what

    // options {
    //     disableConcurrentBuilds()
    //     buildDiscarder(logRotator(numToKeepStr: '10'))
    // }

    stages {
        stage('Dependencies') {
            agent {
                label 'equipo01'
            }
            steps {
                sh 'docker build -t ejemplo-python:latest .'
            }
            post{
                always{
                    echo "====++++always++++===="
                }
                success{
                    echo "====++++A executed succesfully++++===="
                }
                failure{
                    echo "====++++A execution failed++++===="
                }
            }
        }

    //     stage('Build') {
    //         steps {
    //             createPipelineTriggers()
    //             sh 'mvn clean install -DskipTests'
    //             archiveArtifacts '**/target/*.*ar'
    //         }
    //     }

    //     stage('Tests') {
    //         parallel {
    //             stage('Unit Test') {
    //                 steps {
    //                     sh 'mvn test'
    //                 }
    //             }
    //             stage('Integration Test') {
    //                 when { expression { return isTimeTriggeredBuild() } }
    //                 steps {
    //                     sh 'mvn verify -DskipUnitTests -Parq-wildfly-swarm '
    //                 }
    //             }
    //         }
    //     }
    // }

    // post {
    //     always {
    //         // Archive Unit and integration test results, if any
    //         junit allowEmptyResults: true,
    //                 testResults: '**/target/surefire-reports/TEST-*.xml, **/target/failsafe-reports/*.xml'
    //         mailIfStatusChanged env.EMAIL_RECIPIENTS
    //     }
    // }

        // stage('Dependencies') {
        //     agent {
        //         docker {
        //             label 'equipo01'
        //             image 'python:3.7.3-alpine3.10'
        //         }
        //     }
        //     steps {
        //         sh 'id'
        //         sh 'pwd'
        //         sh 'ls -alh'
        //         sh 'pip3 install --upgrade pip'
        //         sh 'pip3 install --no-cache-dir -r requirements.txt'
        //         sh 'python3 scripts/generate_secret_key.py'
        //     }
        //     post{
        //         always{
        //             echo "====++++always++++===="
        //         }
        //         success{
        //             echo "====++++A executed succesfully++++===="
        //         }
        //         failure{
        //             echo "====++++A execution failed++++===="
        //         }
        //     }
        // }

// https://go.cloudbees.com/docs/plugins/docker-workflow/#docker-workflow-sect-build
//   git '…'
//   def newApp = docker.build "mycorp/myapp:${env.BUILD_TAG}"
//   newApp.push() // record this snapshot (optional)
//   stage 'Test image'
//   // run some tests on it (see below), then if everything looks good:
//   stage 'Approve image'
//   newApp.push 'latest'
    }
}
