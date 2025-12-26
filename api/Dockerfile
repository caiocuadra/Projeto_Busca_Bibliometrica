FROM php:8.4-fpm-alpine

# Dependências do sistema
RUN apk add --no-cache \
    nginx \
    supervisor \
    bash \
    icu-dev \
    libzip-dev \
    oniguruma-dev \
    postgresql-dev

# Extensões PHP
RUN docker-php-ext-install \
    pdo \
    pdo_pgsql \
    intl \
    zip \
    mbstring \
    opcache

# Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

COPY . .

RUN composer install --no-dev --optimize-autoloader

# Permissões
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 775 storage bootstrap/cache

# Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Supervisor (nginx + php-fpm)
COPY supervisord.conf /etc/supervisord.conf

EXPOSE 83

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
