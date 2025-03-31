FROM jupyter/base-notebook:latest

USER root
RUN apt-get update \
  && apt-get install -y \
  curl \
  nano \
  vim \
  unzip \
  && apt-get clean \
  && apt-get -y autoremove

RUN pip install --upgrade jupyterlab==4.3.6 
RUN pip install jupyterlab-bxplorer-v2==0.2.7