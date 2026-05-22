export const environment = {
	production: true,
	pingAicBaseUrl: '',
	oidc: {
		issuer: 'https://<tenant>.id.forgerock.io:443/am/oauth2/<realm>',
		clientId: '<spa-client-id>',
		scope: 'openid profile email fr:idm:*',
		responseType: 'code',
		redirectUri: 'https://<your-app-host>/auth/callback',
		postLogoutRedirectUri: 'https://<your-app-host>/login',
		loginUrl: 'https://<tenant>.id.forgerock.io:443/am/oauth2/<realm>/authorize',
		tokenEndpoint: 'https://<tenant>.id.forgerock.io:443/am/oauth2/<realm>/access_token',
		userinfoEndpoint: 'https://<tenant>.id.forgerock.io:443/am/oauth2/<realm>/userinfo',
		logoutUrl: 'https://<tenant>.id.forgerock.io:443/am/oauth2/<realm>/connect/endSession',
		jwksUri: 'https://<tenant>.id.forgerock.io:443/am/oauth2/<realm>/connect/jwk_uri',
		requireHttps: true,
		strictDiscoveryDocumentValidation: false,
	}
};
