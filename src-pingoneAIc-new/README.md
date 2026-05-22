# PingoneAicPortal

This Angular application now uses PingOne Advanced Identity Cloud as its login provider through OIDC Authorization Code flow with PKCE.

## Application setup

Update the OIDC placeholders in `src/environments/environment.ts` and `src/environments/environment.prod.ts`.

```ts
oidc: {
	issuer: 'https://<tenant>.id.forgerock.io/am/oauth2/realms/root/realms/alpha',
	clientId: '<spa-client-id>',
	scope: 'openid profile email fr:idlm:*',
	responseType: 'code',
	redirectUri: 'http://localhost:4200/auth/callback',
	postLogoutRedirectUri: 'http://localhost:4200/login'
}
```

Set `pingAicBaseUrl` if your Angular app should call the PingOne AIC APIs directly with an absolute URL. Leave it empty to use the Angular dev proxy for relative `/openidm` requests.

If you use the dev proxy, update `proxy.conf.json` so the `/openidm` target matches your PingOne AIC tenant host.

## PingOne AIC console steps

1. Sign in to the PingOne Advanced Identity Cloud admin console for the tenant that will authenticate this application.
2. Open the applications area and create a new application for a browser-based client. Use a Single Page Application or public OIDC client type.
3. Enable `Authorization Code` as the grant type and require `PKCE`. Do not use a client secret in the Angular application.
4. Add redirect URIs for every environment that will sign in. At minimum add `http://localhost:4200/auth/callback` for local development.
5. Add post-logout redirect URIs. At minimum add `http://localhost:4200/login` for local development.
6. Configure the scopes that this app needs. The Angular app is set to request `openid profile email fr:idlm:*` by default. Replace `fr:idlm:*` with a narrower scope if your tenant exposes a more limited IDM API scope.
7. Assign the hosted login journey or authentication tree that should run when users sign in.
8. If your tenant protects IDM or REST APIs with OAuth scopes, make sure the application is allowed to receive the scopes required for `/openidm` access.
9. Copy the application `clientId` and the realm `issuer` URL into the environment files in this project.
10. If you have separate development and production applications in PingOne AIC, use the correct client IDs and redirect URLs in each Angular environment file.

## Realm and issuer notes

The sample issuer in the environment files assumes the `alpha` realm:

```text
https://<tenant>.id.forgerock.io/am/oauth2/realms/root/realms/alpha
```

If your journeys and OAuth client live in a different realm, replace the realm segment accordingly.

## Local development

Install dependencies and start the app:

```bash
npm install
npm start
```

Open `http://localhost:4200/login` and use the `Sign In with PingOne` button.

## Build

```bash
npm run build
```
