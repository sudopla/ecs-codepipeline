FROM centos
EXPOSE 80
RUN \
  yum update -y && \
  yum install nginx -y && \
  yum install python3 -y && \ 
  pip3 install boto3 &&\
  pip3 install gunicorn && \
  pip3 install django

COPY app_code/ /usr/src/app/
COPY nginx.conf /etc/nginx/
COPY init_script.sh init_script.sh
CMD ["/init_script.sh"]
