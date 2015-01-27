FROM malev/freeling
MAINTAINER marcosvanetta@gmail.com

RUN locale-gen en_US.UTF-8
ADD ./freeling /freeling

ENV FREELINGCUSTOM /freeling
ENV FREELINGSHARE /usr/local/share/freeling

EXPOSE 50005
CMD analyzer -f /freeling/config/es.cfg --server --port 50005 --workers 2 --queue 1 --outf tagged --nec --noflush --inpf plain
