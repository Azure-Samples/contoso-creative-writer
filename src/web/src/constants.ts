import { githubDevSubsPort } from "./utils/ghutils";

const hostname = window.location.hostname;
const apiPort = 8000


const endpoint = (hostname === 'localhost' || hostname === '127.0.0.1')
    ? `http://localhost:${apiPort}`
    : hostname.endsWith('github.dev') 
    ? `${githubDevSubsPort(hostname, apiPort)}/`
    : "api/article";

export { endpoint };