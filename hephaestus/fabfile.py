from fabric.api import *

env.hosts = "analiceme.cloudapp.net"
env.user = "deploy"
env.key_filename = "~/.ssh/myPrivateKey.key"
env.port = "63478"

def install(packages):
    packages = ['docker.io']
    sudo('apt-get update')
    sudo('apt-get install -y ' + ' '.join(packages))

def deploy():
    put('config.dat', '~/')
    sudo('docker pull malev/hephaestus:latest')
    sudo('docker pull malev/freeling-custom:latest')

    with settings(warn_only=True):
        sudo('docker rm -f freeling')
        sudo('docker rm -f hephaestus-freeling-1')
        sudo('docker rm -f hephaestus-freeling-2')
        sudo('docker rm -f hephaestus-database-1')
        sudo('docker rm -f hephaestus-database-2')
        sudo('docker rm -f hephaestus-database-3')
        sudo('docker rm -f hephaestus-database-4')
        sudo('docker rm -f hephaestus-io-1')
        sudo('docker rm -f hephaestus-io-2')
        sudo('docker rm -f hephaestus-io-3')
        sudo('docker rm -f hephaestus-io-4')
        sudo('docker rm -f hephaestus-text_extraction-1')
        sudo('docker rm -f hephaestus-text_extraction-2')
        sudo('docker rm -f hephaestus-calculation-1')
        sudo('docker rm -f hephaestus-calculation-2')

    sudo('docker run -d --name freeling -p 50005:50005 malev/freeling-custom')
    run('echo FREELING_HOST="$(sudo docker inspect --format \'{{ .NetworkSettings.IPAddress }}\' freeling)" >> config.dat')

    sudo('docker run -d --env-file=config.dat --name=hephaestus-freeling-1 -v ~/log:/app/hephaestus/log -e QUEUE=freeling malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=hephaestus-freeling-2 -v ~/log:/app/hephaestus/log -e QUEUE=freeling malev/hephaestus bundle exec rake resque:work')

    sudo('docker run -d --env-file=config.dat --name=hephaestus-database-1 -v ~/log:/app/hephaestus/log -e QUEUE=database malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=hephaestus-database-2 -v ~/log:/app/hephaestus/log -e QUEUE=database malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=hephaestus-database-3 -v ~/log:/app/hephaestus/log -e QUEUE=database malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=hephaestus-database-4 -v ~/log:/app/hephaestus/log -e QUEUE=database malev/hephaestus bundle exec rake resque:work')


    sudo('docker run -d --env-file=config.dat --name=hephaestus-io-1 -v ~/log:/app/hephaestus/log -e QUEUE=io malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=hephaestus-io-2 -v ~/log:/app/hephaestus/log -e QUEUE=io malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=hephaestus-io-3 -v ~/log:/app/hephaestus/log -e QUEUE=io malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=hephaestus-io-4 -v ~/log:/app/hephaestus/log -e QUEUE=io malev/hephaestus bundle exec rake resque:work')


    sudo('docker run -d --env-file=config.dat --name=hephaestus-text_extraction-1 -v ~/log:/app/hephaestus/log -e QUEUE=text_extraction malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=hephaestus-text_extraction-2 -v ~/log:/app/hephaestus/log -e QUEUE=text_extraction malev/hephaestus bundle exec rake resque:work')

    sudo('docker run -d --env-file=config.dat --name=hephaestus-calculation-1 -v ~/log:/app/hephaestus/log -e QUEUE=calculation malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=hephaestus-calculation-2 -v ~/log:/app/hephaestus/log -e QUEUE=calculation malev/hephaestus bundle exec rake resque:work')
