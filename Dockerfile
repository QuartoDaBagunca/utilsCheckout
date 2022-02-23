# docker image [NEW]
FROM datamechanics/spark:3.1-latest

# usando o usuario root
USER root:root

# definindo variaveis de ambiente
ENV AWS_DEFAULT_REGION us-east-1

# instalando awscli e o nano
RUN apt-get update \
&& apt-get install awscli -y \
&& apt-get install nano -y

# instalando bibliotecas dobootstrap_emr.sh
RUN pip install --upgrade pip \ 
&& pip3 install boto3 \ 
&& pip3 install py4j \ 
&& pip3 install chispa \ 
&& pip3 install pymsteams

# definindo workspace
COPY ./jars/ngdbc-2.8.14.jar /opt/spark/jars/
COPY ./src/ /opt/spark/python/src/
COPY ./spark_main.py /opt/spark/python/
COPY ./test.py /opt/spark/python/
WORKDIR /opt/spark/python

# RUN chmod 777 src/utils