import json
import urlparse
import urllib

import oauth2 as oauth

## If you're actually processing requests, you'll want this
# import simplejson 


request_token_url = 'https://api.dropbox.com/1/oauth/request_token'
authorize_url     = 'https://www.dropbox.com/1/oauth/authorize'
access_token_url  = 'https://api.dropbox.com/1/oauth/access_token'

### GET A REQUEST TOKEN ###

consumer = oauth.Consumer(key="b4k7ni0mlnwplv0", secret="ui02su5h4i4ttlc")

client = oauth.Client(consumer)

response = client.request(request_token_url, "GET")[1]
request_token = dict(urlparse.parse_qsl(response))

token = oauth.Token(
  request_token['oauth_token'],
  request_token['oauth_token_secret']
)


# AUTHORIZE
print 'Please go to %s?oauth_token=%s' % (authorize_url, request_token['oauth_token'])

raw_input('OK ?')


# ACCESS TOKEN
token = oauth.Token(request_token['oauth_token'],
    request_token['oauth_token_secret'])
#token.set_verifier()
client = oauth.Client(consumer, token)

resp, content = client.request(access_token_url, "POST")
access_token = dict(urlparse.parse_qsl(content))


token = oauth.Token(
    access_token['oauth_token'],
    access_token['oauth_token_secret']
  )
client = oauth.Client(consumer, token)

print client.request('https://api.dropbox.com/1/metadata/sandbox/', 'GET')
