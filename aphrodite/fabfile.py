from fabric.api import *

env.hosts = "analiceme.cloudapp.net"
env.user = "deploy"
env.key_filename = "~/.ssh/myPrivateKey.key"
env.port = "22"

def install(packages):
    packages = ['nginx', 'docker.io']
    sudo('apt-get update')
    sudo('apt-get install -y ' + ' '.join(packages))
    put('nginx.conf', '/etc/nginx/sites-enabled/default')
    sudo('service nginx restart')

def deploy():
    put('config.dat', '~/')
    sudo('docker pull malev/aphrodite:latest')
    sudo('docker rm -f aphrodite-1')
    sudo('docker run -d -p 3001:8080 --env-file=config.dat --name=aphrodite-1 -v ~/log:/app/aphrodite/log malev/aphrodite')
    sudo('docker rm -f aphrodite-2')
    sudo('docker run -d -p 3002:8080 --env-file=config.dat --name=aphrodite-2 -v ~/log:/app/aphrodite/log malev/aphrodite')
    sudo('docker rm -f aphrodite-3')
    sudo('docker run -d -p 3003:8080 --env-file=config.dat --name=aphrodite-3 -v ~/log:/app/aphrodite/log malev/aphrodite')

def deploy_schedulers():
    put('config.dat', '~/')
    sudo('docker pull malev/hephaestus:latest')
    sudo('docker rm -f scheduler-1')
    sudo('docker rm -f scheduler-2')
    sudo('docker rm -f scheduler-3')
    sudo('docker rm -f scheduler-4')
    sudo('docker rm -f scheduler-5')
    sudo('docker run -d --env-file=config.dat --name=scheduler-1 -v ~/log:/app/hephaestus/log malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=scheduler-2 -v ~/log:/app/hephaestus/log malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=scheduler-3 -v ~/log:/app/hephaestus/log malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=scheduler-4 -v ~/log:/app/hephaestus/log malev/hephaestus bundle exec rake resque:work')
    sudo('docker run -d --env-file=config.dat --name=scheduler-5 -v ~/log:/app/hephaestus/log malev/hephaestus bundle exec rake resque:work')
