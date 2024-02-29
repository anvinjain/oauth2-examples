## README

This repo was created for a talk - Primer on OAuth2. It has example client applications using Oauth2 for user and service authentication.

```
pipenv install --python=3.11
pipenv shell
pipenv install flask #installing specific package
```


-------

### Contents of the talk

**OAuth2 Basic - Authentication, Authorization, Multiple Flows**  
* https://auth0.com/intro-to-iam/what-is-oauth-2
* https://auth0.com/docs/get-started/authentication-and-authorization-flow/which-oauth-2-0-flow-should-i-use

**Authorization code flow**  
* Sign in with Github demo. Login and then cookie inspection for auto login  
* Sign in With Facebook demo. Auto login and token [Introspection](https://developers.facebook.com/tools/explorer/?method=GET&path=debug_token%3Finput_token%3DEAAXCwOAEi9EBO5Pjf5CyiTgqEZB6n7GcrHL5QfZAu6wBqvBsDUW2Hus4VSFTTQ5vx8zo5Njo5rh0n1J59O7kbgjYlTu031MJUYx9V010DjwKKiMHyJKP9TqhvQigmuyEKyfq9bm5KfiDy1NwDF5bZBb7c1LVVgfYqqjoPFQotWIG4ftOv0sWVF8NBYcBh7XDBmKB50R3kUuQiUhueda6JR1OEC9vye3tVnTlFNKZAl5d3VZAyIOMm9ZAIKl5ll75gZD&version=v19.0)
* Portability of access token, security implications

**Client Credentials flow**  
Facebook App Management demo