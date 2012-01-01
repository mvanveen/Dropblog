'''Dropbox Client library

'''

import pickle
import simplejson as json
import urlparse
import urllib

import oauth2 as oauth

request_token_url = 'https://api.dropbox.com/1/oauth/request_token'
authorize_url     = 'https://www.dropbox.com/1/oauth/authorize'
access_token_url  = 'https://api.dropbox.com/1/oauth/access_token'

### GET A REQUEST TOKEN ###


def get_token_and_consumer():
  consumer = oauth.Consumer(key="b4k7ni0mlnwplv0", secret="ui02su5h4i4ttlc")

  request_token = dict(
    urlparse.parse_qsl(
      oauth.Client(consumer).request(request_token_url, "GET")[1]
    ))

  token = oauth.Token(
    request_token['oauth_token'],
    request_token['oauth_token_secret']
  )

  print 'Please go to %s?oauth_token=%s' % (authorize_url, request_token['oauth_token'])
  raw_input('OK ?')

  return consumer, token



## AUTHORIZE


# ACCESS TOKEN

def get_access_token():
  cred = get_token_and_consumer()
  resp, content = oauth.Client(*cred).request(access_token_url, "POST")
  access_token = dict(urlparse.parse_qsl(content))
  
  token = oauth.Token(
      access_token['oauth_token'],
      access_token['oauth_token_secret']
    )

  return oauth.Client(cred[0], token)


def write_client():
  fileObj = open('lol.pik', 'w')
  fileObj.write(pickle.dumps(get_access_token()))


def get_client():
  fileObj = open('lol.pik', 'r')
  return pickle.loads(fileObj.read())


