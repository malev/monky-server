FROM ubuntu:14.04
MAINTAINER marcosvanetta@gmail.com

RUN locale-gen en_US.UTF-8
RUN apt-get update -q
RUN apt-get install -y git git-core wget
RUN apt-get install -y build-essential libicu-dev libboost1.54-all-dev libboost-regex1.54-dev libboost-regex-dev libboost-system-dev libboost-program-options-dev libboost-thread-dev zlib1g-dev automake autoconf libtool

ADD freeling-3.1.tar.gz /tmp/
ADD automake_options.am /tmp/freeling-3.1/src/

WORKDIR /tmp/freeling-3.1
RUN aclocal; libtoolize; autoconf; automake -a
RUN ./configure
RUN make
RUN make install
