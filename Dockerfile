# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

# https://hub.docker.com/_/ubuntu/tags
FROM centos:centos8

RUN yum -y install python3-pip

RUN pip3 install flask
