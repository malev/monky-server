import os
import yaml
from fabric.api import *
from dependencies import *

environment = 'staging'
if 'ENV' in os.environ:
    environment = os.environ['ENV']

stream = open('config.yml', 'r')
config = yaml.load(stream)

env.hosts = [config[environment]['HostName']]
env.user = config[environment]['User']
env.key_filename = config[environment]['IdentifyKey']
env.port = config[environment]['Port']

def install(packages):
    run('sudo apt-get install -y ' + ' '.join(packages))

def swap():
    sudo('dd if=/dev/zero of=/swapfile bs=1024 count=1024k')
    sudo('mkswap /swapfile')
    sudo('swapon /swapfile')
    sudo('echo "/swapfile       none    swap    sw      0       0 " >> /etc/fstab')
    sudo('echo 10 | sudo tee /proc/sys/vm/swappiness')
    sudo('echo vm.swappiness = 10 | sudo tee -a /etc/sysctl.conf')
    sudo('chown root:root /swapfile')
    sudo('chmod 0600 /swapfile')

def run_rbenv(cad):
    run('PATH="$HOME/.rbenv/bin:$PATH" ' + cad)

def dot_files():
    install(['exuberant-ctags', 'ack-grep'])
    run('git clone https://github.com/malev/dotfiles.git')
    run('ln -s ~/dotfiles/vimrc ~/.vimrc')
    run('ln -s ~/dotfiles/tmux.conf ~/.tmux.conf')
    run('ln -s ~/dotfiles/gitconfig ~/.gitconfig')

def freeling():
    run('apt-get update')
    run('apt-get install -y ' + ' '.join(freeling_dependencies))
    run('wget https://s3.amazonaws.com/src.codingnews.info/freeling-3.1.tar.gz')
    run('tar xvzf freeling-3.1.tar.gz')
    put('files/automake_options.am', 'freeling-3.1/src/')
    run('cd freeling-3.1 && aclocal; libtoolize; autoconf; automake -a')
    run('cd freeling-3.1 && ./configure')
    run('cd freeling-3.1 && make')
    run('cd freeling-3.1 && make install')
    run('locale-gen en_US.UTF-8')

def sudo_freeling():
    sudo('apt-get update')
    sudo('apt-get install -y ' + ' '.join(freeling_dependencies))
    run('wget https://s3.amazonaws.com/src.codingnews.info/freeling-3.1.tar.gz')
    run('tar xvzf freeling-3.1.tar.gz')
    put('files/automake_options.am', 'freeling-3.1/src/')
    run('cd freeling-3.1 && aclocal; libtoolize; autoconf; automake -a')
    run('cd freeling-3.1 && ./configure')
    run('cd freeling-3.1 && make')
    sudo('cd freeling-3.1 && make install')
    sudo('locale-gen en_US.UTF-8')

def nodejs():
    run('git clone https://github.com/creationix/nvm.git ~/.nvm')
    run("echo 'source ~/.nvm/nvm.sh' >> .bashrc")
    run('source ~/.nvm/nvm.sh && nvm install 0.10')
    run('source ~/.nvm/nvm.sh && nvm alias default 0.10')

def ruby():
    install(ruby_dependencies)
    run('git clone https://github.com/sstephenson/rbenv.git ~/.rbenv')
    run("echo 'export PATH=\"$HOME/.rbenv/bin:$PATH\"' >> ~/.bashrc")
    run("echo 'eval \"$(rbenv init -)\"' >> ~/.bashrc")
    run('git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build')

    run_rbenv('rbenv install 2.1.2')
    run_rbenv('rbenv global 2.1.2')
    with settings(warn_only=True):
        run('export PATH=$HOME/.rbenv/bin:$PATH')
        run('eval "$(~/.rbenv/bin/rbenv init -)"')
    run('~/.rbenv/shims/gem install bundler')
    run('~/.rbenv/bin/rbenv rehash')

def elasticsearch():
    install(elasticsearch_dependencies)
    run('wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.0.deb')
    sudo('dpkg -i elasticsearch-1.3.0.deb')
    sudo('echo "script.disable_dynamic: false" /etc/elasticsearch/elasticsearch.yml')
    sudo('echo "network.bind_host: 127.0.0.1" /etc/elasticsearch/elasticsearch.yml')

def remove_user(username="deploy"):
    sudo('userdel -r ' + username)

def create_user(username="deploy"):
    key = ""
    with open(os.getenv("HOME") + '/.ssh/id_rsa.pub', 'r') as content_file:
        key = content_file.read()

    run('useradd ' + username +' -m')
    run('mkdir /home/' + username + '/.ssh')
    run('passwd ' + username)
    run('echo "' + key + '" > /home/' + username + '/.ssh/authorized_keys')
    run('chmod 700 /home/' + username +'/.ssh')
    run('chown ' + username +':' + username +' /home/' + username+ ' -R')
    run('adduser ' + username + ' sudo')
    run('usermod -s /bin/bash ' + username)

def install_basic_packages():
    install(basic_packages)

def closing_ssh():
    sudo("sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config")
    sudo("sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
    sudo('service ssh restart')

def docsplit():
    install(docsplit_dependencies)

def update():
    sudo('apt-get update -y')
    sudo('apt-get upgrade -y')

def hephaestus():
    update()
    install(basic_packages)
    install(docsplit_dependencies)
    sudo_freeling()
    ruby()
