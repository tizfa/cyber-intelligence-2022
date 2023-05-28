# Starting from Ubuntu image...
FROM ubuntu

# Install Python 3.9 and default Java JDK.
RUN apt-get update && \
	apt-get -y install python3.9 python3-pip default-jdk wget unzip && \
	apt-get clean

# Install Nifi
RUN wget -P /opt https://archive.apache.org/dist/nifi/1.16.0/nifi-1.16.0-bin.zip
RUN unzip /opt/nifi-1.16.0-bin.zip -d /opt
RUN echo "nifi.web.https.host=0.0.0.0" >> /opt/nifi-1.16.0/conf/nifi.properties
RUN echo "nifi.web.https.network.interface.default=eth0" >> /opt/nifi-1.16.0/conf/nifi.properties
RUN echo "nifi.web.https.network.interface.lo=lo" >> /opt/nifi-1.16.0/conf/nifi.properties


# Install all required Pytjhon modules.
RUN apt-get install -y libicu-dev python3-icu && pip3 install gensim nltk polyglot six requests morfessor readability-lxml bs4 praw pandas urllib3==1.26.6

# Install pycld2
RUN ln -s /usr/bin/python3 /usr/bin/python && apt-get install unzip && \
	wget https://github.com/aboSamoor/pycld2/archive/refs/heads/master.zip -P /root && unzip /root/master.zip -d /root && \
	cd /root/pycld2-master/;make build

# Initialize polyglot library.
RUN polyglot download LANG:it LANG:en

# Reclaim disk space.
RUN apt-get clean && rm -fr /opt/nifi-1.16.0-bin.zip

RUN /opt/nifi-1.16.0/bin/nifi.sh set-single-user-credentials user cyberintelligence
COPY login-identity-providers.xml /opt/nifi-1.16.0/conf/

RUN ln -s /opt/nifi-1.16.0 /opt/nifi

# Copy material for practice
#RUN mkdir -p /home/cint
#COPY cint /home/cint



EXPOSE 8080
EXPOSE 8443
EXPOSE 9088
EXPOSE 6342


CMD /opt/nifi-1.16.0/bin/nifi.sh run


