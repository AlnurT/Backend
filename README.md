### Общая сеть между контейнерами:
`docker network create myNetwork`

### Контейнер с базой данных Postgres:
`docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16`

### Контейнер с Redis:
`docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4`

### Контейнер с бэком:
`docker compose up -d --build`

### Контейнер с nginx:
`docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=myNetwork \
    --rm -p 80:80 nginx`

### Запуск раннера:
`docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:alpine`

### Регистрация раннера:
`docker run --rm -it \
    -v /srv/gitlab-runner/config:/etc/gitlab-runner \
    gitlab/gitlab-runner:alpine register`

### Изменение конфига:
`nano /srv/gitlab-runner/config/config.toml`

Меняем
`volumes = ["/cache"] `
на

`volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]`
