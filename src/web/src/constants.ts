import { githubDevSubsPort } from "./utils/ghutils";

const hostname = window.location.hostname;
const apiPort = 8000


const endpoint = 
    // @ts-expect-error
    window['endpoint'] ? window['endpoint']
    : (hostname === 'localhost' || hostname === '127.0.0.1')
    ? `http://localhost:${apiPort}`
    : hostname.endsWith('github.dev') 
    ? `${githubDevSubsPort(hostname, apiPort)}/`
    : "api/article";

export { endpoint };

const image_endpoint = 
    // @ts-expect-error
    window['endpoint'] ? window['endpoint']
    : (hostname === 'localhost' || hostname === '127.0.0.1')
    ? `http://localhost:${apiPort}`
    : hostname.endsWith('github.dev') 
    ? `${githubDevSubsPort(hostname, apiPort)}/`
    : "api/upload-image";

export { image_endpoint };

// uploadLocation.ts
let uploadLocation: string | null = null;

export const setUploadLocation = (location: string) => {
    uploadLocation = location;
};

export const getUploadLocation = () => uploadLocation || "";