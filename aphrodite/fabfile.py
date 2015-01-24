from fabric.api import *

env.hosts = "example.org"
env.user = "user"
env.key_filename = "~/.ssh/myPrivateKey.key"
env.port = "22"

def install(packages):
    packages = ['nginx', 'docker.io']
    sudo('apt-get update')
    sudo('apt-get install -y ' + ' '.join(packages))
    put('nginx.conf', '/etc/nginx/sites-enabled/default')
    sudo('service nginx restart')
    sudo('docker login')

def deploy():
    put('config.dat', '~/')
    sudo('docker pull malev/aphrodite')
    sudo('docker rm -f aphrodite-1')
    sudo('docker run -d -p 3001:8080 --env-file=config.dat --name=aphrodite-1 malev/aphrodite')
    sudo('docker rm -f aphrodite-2')
    sudo('docker run -d -p 3002:8080 --env-file=config.dat --name=aphrodite-2 malev/aphrodite')
    sudo('docker rm -f aphrodite-3')
    sudo('docker run -d -p 3003:8080 --env-file=config.dat --name=aphrodite-3 malev/aphrodite')
