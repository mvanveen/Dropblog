import json

import dropbox_client

def test_get_url():
  client = dropbox_client.get_client()
  assert json.loads(client.request('https://api.dropbox.com/1/account/info', 'GET')[1]) is not None

  
