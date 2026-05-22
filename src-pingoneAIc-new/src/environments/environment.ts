export const environment = {
  production: false,
  pingAicBaseUrl: '',
  oidc: {
    issuer: 'https://openam-bruneishell-ase1-dev.id.forgerock.io:443/am/oauth2/alpha',
    clientId: 'OIDCLogin',
    scope: 'openid profile email fr:idm:*',
    responseType: 'code',
    redirectUri: 'http://localhost:4200/auth/callback',
    postLogoutRedirectUri: 'http://localhost:4200/login',
    loginUrl: 'https://openam-bruneishell-ase1-dev.id.forgerock.io:443/am/oauth2/alpha/authorize',
    tokenEndpoint: 'https://openam-bruneishell-ase1-dev.id.forgerock.io:443/am/oauth2/alpha/access_token',
    userinfoEndpoint: 'https://openam-bruneishell-ase1-dev.id.forgerock.io:443/am/oauth2/alpha/userinfo',
    logoutUrl: 'https://openam-bruneishell-ase1-dev.id.forgerock.io:443/am/oauth2/alpha/connect/endSession',
    jwksUri: 'https://openam-bruneishell-ase1-dev.id.forgerock.io:443/am/oauth2/alpha/connect/jwk_uri',
    requireHttps: false,
    strictDiscoveryDocumentValidation: false,
  }
};
