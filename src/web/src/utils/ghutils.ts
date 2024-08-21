function githubDevSubsPort(hostname: string, port: number): string {
    const regex = /-[0-9]{4,6}/gm;
    const subst = `-${port}`;
    let result = hostname.replace(regex, subst);
    if (!result.startsWith("https://")) {
        result = "https://"+ result;
    }
    return result;    
}

export { githubDevSubsPort }