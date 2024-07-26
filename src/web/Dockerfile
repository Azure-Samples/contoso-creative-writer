FROM nginx:alpine

WORKDIR /app

COPY dist/* .
COPY dist/assets/* ./assets/

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]