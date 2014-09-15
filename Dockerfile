FROM ubuntu:12.04
MAINTAINER Marcos Vanetta <marcosvanetta@gmail.com>

# http://nlp.lsi.upc.edu/freeling/index.php?option=com_simpleboard&Itemid=65&func=view&id=3545&view=flat&catid=5
RUN locale-gen en_US.UTF-8
RUN apt-get update
RUN apt-get install -y build-essential libxml2-dev libxslt1-dev libicu-dev zlib1g-dev libboost-all-dev libboost-thread-dev

ADD src/freeling-3.1.tar.gz /tmp/

RUN ls /tmp
RUN cd /tmp/freeling-3.1 && \
    ./configure && \
    make && \
    make install && \
    rm -rf /tmp/freeling-3.1

ENV FREELINGSHARE /usr/local/share/freeling/

EXPOSE 50005

ENTRYPOINT analyzer
CMD ['-f', '/usr/local/share/freeling/config/es.cfg', '--server', '--port', '50005']
