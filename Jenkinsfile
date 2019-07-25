pipeline {
    agent {
        label 'docker && equipo01'
    }
// Simple vs Double quotes
// https://stackoverflow.com/questions/37464887/vs-vs-in-groovy-when-to-use-what

    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Dependencies') {
            steps {
                agent {
                    docker {
                        image 'python:3.7.3-alpine3.10'
                    }
                }
                sh 'pip install --upgrade pip'
                sh 'pip3 install --no-cache-dir -r requirements.txt'
                sh 'ls -alh'
                sh 'python3 scripts/generate_secret_key.py'
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
    }
}
