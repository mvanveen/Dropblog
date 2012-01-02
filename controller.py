import datetime
import simplejson as json
import logging

from bottle import route, run, request
from google.appengine.api import memcache
import markdown

from models import (
  get_header,
  get_index,
  get_footer,
  get_post_front_matter,
  get_post,
  get_posts,
  get_posts_html,
  get_posts_time,
  get_post_no,
  split_file
)


def render_item(item):
  front_item = get_post_front_matter(item['path'])
  return  '''
    <b>%s</b><br />
    <i>%s</i><br />
    Author: %s <br />
    <br />
  ''' %(
    front_item['title'],
    str(datetime.datetime.fromtimestamp(front_item['time'])) ,
    front_item['author'] + markdown.markdown(
      split_file(get_post(item['path']))[1]
    ))


def render_front():
  items = reversed(get_posts_time()[:10])
  rendered = []

  for item in items: 
    rendered.append(render_item(item))

  return "<hr style='border 1px solid black;margin:0;'/>".join(rendered)
  

@route('/')
@route('/index')
def get_root():
  overwrite = request.query.overwrite or False
  return ''.join((
    get_header(overwrite=overwrite),
    render_front(),
    get_footer(overwrite=overwrite)
  ))


@route('/posts')
def route_posts(fun=get_posts_html, **kw):
  '''Returns a JSON dictionary about current posts'''

  posts = get_posts_time()
  overwrite = request.query.overwrite or False
  kw['overwrite'] = overwrite

  logging.info('overwrite: %s' % overwrite)

  posts = [
    get_post_front_matter(
      post.get('path'),
      overwrite=overwrite
    ) for post in posts
  ]
  
  req_type = request.query.type
  if req_type == 'json':
  
    return {
      'posts': [{
          'id': id_val,
          'time': x.get('time'),
          'last_modified': x.get('time'),
          'title': x.get('title')
        } for id_val, x in enumerate(posts)
      ]}

  else:
    return (
      ''.join((
      get_header(**kw),
      fun(**kw),
      '<ul>%s</ul>' % '\n'.join(
      ["<li><a href='/posts/%s'>%s</a></li>" % 
        (pid, x.get('title')) for pid, x in enumerate(posts)
      ]),
      get_footer(**kw)
    )))
 

@route('/posts/:post_id')
def route_post_md(post_id=None):
  req_type = request.query.type

  if req_type == 'json':
    return {'post': get_post_no(post_id)}
  else:
    template  = memcache.get('')
    overwrite = request.query.overwrite or False

    return ''.join((
      get_header(overwrite=overwrite),
      markdown.markdown(
        split_file(get_post_no(post_id, overwrite=overwrite))[1]
      ),
      get_footer(overwrite=overwrite)
    ))

run(server='gae')
