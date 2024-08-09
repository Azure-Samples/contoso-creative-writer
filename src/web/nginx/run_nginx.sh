sed -i "s,/\*INIT_SECTION\*/,window['endpoint']='${API_ENDPOINT}'," /app/index.html
nginx -g "daemon off;"
