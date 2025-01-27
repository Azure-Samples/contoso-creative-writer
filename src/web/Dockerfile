# Build stage
FROM node:20.11.1-alpine3.19 AS ui
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci

# Copy the rest of your application's source code
COPY . .

# Build the project
RUN npm run build

FROM nginx:alpine

WORKDIR /app

# Copy UI static files
COPY --from=ui /app/dist/* ./
COPY --from=ui /app/dist/assets/* ./assets/

EXPOSE 80

COPY ./nginx/nginx.conf /nginx.conf.template
CMD ["/bin/sh" , "-c" , "envsubst < /nginx.conf.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'"]