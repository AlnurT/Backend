git config user.name "Alnur"
git config user.email "alnur.tazhbenov@mail.ru"

docker network create myNetwork

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4

docker build -t booking_image .

docker compose up -d --build

docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=myNetwork \
    --rm -p 80:80 nginx
