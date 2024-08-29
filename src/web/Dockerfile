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

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx/run_nginx.sh /bin/run_nginx.sh

EXPOSE 80
RUN ["chmod", "+x", "/bin/run_nginx.sh"]
CMD ["/bin/run_nginx.sh"]