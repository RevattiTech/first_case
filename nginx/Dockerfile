FROM nginx:1.21-alpine
RUN apk update && apk add openssl


COPY . .


#COPY ./ssl/iddrops_com.key /ssl/iddrops_com.csr
#RUN chmod 400 /ssl/iddrops_com.crt
#RUN chmod 400 /ssl/iddrops_com.ca-bundle


RUN rm /etc/nginx/nginx.conf
COPY /nginx.conf /etc/nginx/

