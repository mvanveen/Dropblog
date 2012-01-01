import logging
import re
import simplejson as json

from google.appengine.api import memcache
import yaml

from dropbox_client import get_client


path_url = 'https://api-content.dropbox.com/1/files/sandbox' # don't add a `/`!
metadata_url = 'https://api.dropbox.com/1/metadata/sandbox/'

client = get_client()
get = lambda x: client.request(x, 'GET')[1]

path_fun = lambda x: x['path']



def get_posts(sort_key=path_fun, overwrite=False):
  url = ''.join((metadata_url, 'posts'))
  logging.info('url is: %s' % url)

  return sorted(
    json.loads(get(url)).get('contents', {}),
    key=sort_key
  )


def get_post_front_matter(file_str, overwrite=False):
  file_str = split_file(get_post(file_str, overwrite=overwrite))
  logging.info(file_str)
  return dict([
    (key.lower(), val) for key, val in yaml.load(file_str[0]).iteritems()
  ])


def sort_time(obj):
  obj = obj.get('path')
  result = split_file(obj)

  frontmatter = get_post_front_matter(result[0])

  found_time = frontmatter['title']
  
  logging.info('time: %s' % found_time)
  return found_time


def get_posts_time(**kw):
  kw.update({'sort_key': sort_time})
  return get_posts(**kw)


def get_post_no(no):
  '''Gets post based off of index number'''

  post = get_posts_time()[int(no)]['path']
  logging.info('getting post: %s' % post)
  return get_post(post)


def get_post(path, overwrite=False):
  assert isinstance(path, basestring), 'Expected path to be a string'

  prefix = 'file_'
  key = ''.join((prefix, path))

  fileObj = memcache.get(key)

  if not fileObj or overwrite:
    logging.info('flushing cache for obj: %s' % path)
    fileObj = get(''.join((path_url, path)))

    result = False
    while not result: 
      result = memcache.set(key, fileObj)
  
  logging.info('fileObj: %s' % fileObj)
  return fileObj


def split_file(file_str):
  result = re.split(r'\n\n', file_str)
  return (result[0], '\n\n'.join(result[1:]))

