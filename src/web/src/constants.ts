import { githubDevSubsPort } from "./utils/ghutils";

const hostname = window.location.hostname;
const apiPort = 8080


const apiEndpoint = (hostname === 'localhost' || hostname === '127.0.0.1')
    ? `http://localhost:${apiPort}/get_article`
    : hostname.endsWith('github.dev') 
    ? `${githubDevSubsPort(hostname, apiPort)}/get_article`
    : "api/get_article";

export { apiEndpoint };
