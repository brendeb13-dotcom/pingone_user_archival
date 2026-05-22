// export const environment = {
//     production: false,
//     pingone: {
//         authUrl: 'https://auth.pingone.com',
//         apiUrl: 'https://api.pingone.com/v1/aic',
//         orgId: 'YOUR_ORG_ID',
//         envId: 'YOUR_ENV_ID',
//         clientId: 'CLIENT_ID',
//         clientSecret: 'CLIENT_SECRET'
//     }
// };
export const environment = {
  production: false,
  // Use Angular dev proxy to avoid CORS in browser. See proxy.conf.json
  pingAicBaseUrl: 'https://openam-bruneishell-ase1-dev.id.forgerock.io',
  backendApiUrl: ''
};