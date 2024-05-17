const hostname = window.location.hostname;
const apiEndpoint = (hostname === 'localhost' || hostname === '127.0.0.1') ? "http://localhost:8080/get_article" : "api/get_article";

export { apiEndpoint };
