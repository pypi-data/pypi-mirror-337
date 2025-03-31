FROM jupyter/base-notebook:latest

ENV AWS_ACCESS_KEY_ID=AKIA3I3VBU4SKSUMJJ4T 
ENV AWS_SECRET_ACCESS_KEY=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 
ENV AWS_DEFAULT_REGION=us-east-1

USER root
RUN apt-get update \
  && apt-get install -y \
  curl \
  nano \
  vim \
  unzip \
  && apt-get clean \
  && apt-get -y autoremove

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
  unzip awscliv2.zip && \
  sudo ./aws/install

RUN echo 'export PATH="/usr/local/aws-cli/v2/current/bin:$PATH"' >> ~/.bashrc
RUN source ~/.bashrc
RUN pip install --upgrade jupyterlab==4.3.6
RUN pip install aws jupyterlab-bxplorer-v2==0.2.14