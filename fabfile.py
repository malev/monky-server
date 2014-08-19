import os
from fabric.api import run, settings, sudo


def install(dependencies):
    run('sudo apt-get install -y ' + ' '.join(dependencies))


def run_rbenv(cad):
    run('PATH="$HOME/.rbenv/bin:$PATH" ' + cad)


def dot_files():
    install(['exuberant-ctags', 'ack-grep'])
    run('git clone https://github.com/malev/dotfiles.git')
    run('ln -s ~/dotfiles/vimrc ~/.vimrc')
    run('ln -s ~/dotfiles/tmux.conf ~/.tmux.conf')
    run('ln -s ~/dotfiles/gitconfig ~/.gitconfig')


def freeling_trunk():
    dependencies = [
        'libxml2-dev', 'libxslt1-dev', 'libicu-dev', 'libboost-all-dev',
        'zlib1g-dev', 'libboost-thread-dev', 'automake', 'autoconf', 'libtool'
    ]
    install(dependencies)
    run('svn checkout http://devel.cpl.upc.edu/freeling/svn/versions/freeling-3.1 freeling-3.1')
    run('cd freeling-3.1 && aclocal; libtoolize; autoconf; automake -a')
    run('cd freeling-3.1 && ./configure')
    run('cd freeling-3.1 && make')
    sudo('cd freeling-3.1 && make install')


def freeling():
    dependencies = ['libxml2-dev', 'libxslt1-dev', 'libicu-dev', 'zlib1g-dev', 'libboost-all-dev', 'libboost-thread-dev']
    install(dependencies)
    run('wget http://devel.cpl.upc.edu/freeling/downloads/32')
    run('mv 32 freeling.tar.gz')
    run('tar xvzf freeling.tar.gz')
    run('cd freeling-3.1 && ./configure')
    run('cd freeling-3.1 && make')
    sudo('cd freeling-3.1 && make install')


def nodejs():
    run('git clone https://github.com/creationix/nvm.git ~/.nvm')
    run("echo 'source ~/.nvm/nvm.sh' >> .bashrc")
    run('source ~/.nvm/nvm.sh && nvm install 0.10')
    run('source ~/.nvm/nvm.sh && nvm alias default 0.10')


def ruby():
    install([
        'build-essential', 'libssl-dev', 'autoconf', 'bison',
        'libyaml-dev', 'libreadline6', 'libreadline6-dev',
        'zlib1g', 'zlib1g-dev'])

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
    dependencies = ['openjdk-7-jdk', 'openjdk-7-jre', 'icedtea-7-plugin']
    install(dependencies)
    run('wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.0.deb')
    run('dpkg -i elasticsearch-1.3.0.deb')
    run('echo "script.disable_dynamic: false" /etc/elasticsearch/elasticsearch.yml')
    run('echo "network.bind_host: 127.0.0.1" /etc/elasticsearch/elasticsearch.yml')


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


def basic_packages():
    dependencies = [
        'build-essential', 'git-core', 'mongodb', 'mongodb-server',
        'redis-server', 'libxml2-dev', 'libxslt1-dev', 'subversion']
    install(dependencies)


def closing_ssh():
    sudo("sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config")
    sudo("sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
    sudo('service ssh restart')

def docsplit():
    dependencies = [
        'graphicsmagick', 'poppler-utils', 'poppler-data', 'ghostscript',
        'pdftk', 'libreoffice'
    ]
    install(dependencies)


def update():
    run('apt-get update -y')
    run('apt-get upgrade -y')


def first_steps(user="deploy"):
    update()
    basic_packages()
    elasticsearch()
    create_user(user)
    closing_ssh()
