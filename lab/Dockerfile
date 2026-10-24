ARG PHP_IMAGE=php:8.4.26-apache
FROM ${PHP_IMAGE}

COPY php-lab.ini /usr/local/etc/php/conf.d/zz-lab.ini
COPY apache-lab.conf /etc/apache2/conf-enabled/zz-lab.conf
COPY mpm-prefork.conf /etc/apache2/mods-available/mpm_prefork.conf
COPY www/ /var/www/html/
