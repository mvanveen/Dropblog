import logging
import re
import simplejson as json

from google.appengine.api import memcache
import yaml

from dropbox_client import get_client


# Dropbox API endpoints
path_url = 'https://api-content.dropbox.com/1/files/sandbox' # don't add a `/`!
metadata_url = 'https://api.dropbox.com/1/metadata/sandbox/'

# Get a dropbox client (pickled)
client = get_client()

# helper to download a RESTFUL endpoint with the GET method.
get = lambda x: client.request(x, 'GET')[1]

# A sorting function for posts. Sorts by filename.
path_fun = lambda x: x['path']


def get_posts(sort_key=path_fun):
  '''Returns posts as a sorted dictionary.

      TODO: add caching

  '''
  url = ''.join((metadata_url, 'posts'))
  logging.info('url is: %s' % url)

  return sorted(
    json.loads(get(url)).get('contents', {}),
    key=sort_key
  )


def get_post_front_matter(file_str, overwrite=False):
  '''Helper function which turns the front-matter of a post into YAML

    *e.g.*

      Title: This is a title         title: This is a title
      Author: This is an author  =>  author: This is an author
      Time: 123456789                time: 123456789

      My great post starts here              ||
                                            \\//

                                      {'title': 'This is a title',
                                        'author': 'This is an author',
                                        'time': 123456789
                                      }
  '''
  file_str = split_file(
    get_post(
      file_str,
      overwrite=overwrite
    ))

  return dict([
    (key.lower(), val) for key, val 
      in yaml.load(file_str[0]).iteritems()
  ])


def sort_time(obj):
  '''Used as a sorting function which returns a post's time: header vlaue

  Side effect: Reads a post to determine its date.

  '''
  obj = obj.get('path')
  result = split_file(obj)

  frontmatter = get_post_front_matter(result[0])

  found_time = frontmatter['time']
  
  logging.info('time: %s' % found_time)
  return int(found_time)


def get_posts_time(**kw):
  '''Sort posts by time header'''

  kw.update({'sort_key': sort_time})
  return get_posts(**kw)


def get_post_no(no, **kw):
  '''Gets post based off of index number'''

  post = get_posts_time()[int(no)]['path']
  logging.info('getting post: %s' % post)
  return get_post(post, **kw)


def get_item(path, overwrite=False):
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
  
  return fileObj


def split_file(file_str):
  result = re.split(r'\n\n', file_str)
  return (result[0], '\n\n'.join(result[1:]))


def get_post(path, **kw):
  return get_item(path, **kw)


def get_header(**kw):
  header = get_item('/templates/header.html', **kw)
  return header


def get_footer(**kw):
  return get_item('/templates/footer.html', **kw)


def get_posts_html(**kw):
  return get_item('/templates/posts.html', **kw)


def get_index(**kw):
  return get_item('/templates/index.html', **kw)
