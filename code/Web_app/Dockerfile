FROM php:7.2-apache

RUN mkdir uploads
RUN chmod 777 uploads
RUN docker-php-ext-install mysqli

COPY . /var/www/html/