import simplejson as json
import logging

from bottle import route, run
import markdown

from models import (
  get_post_front_matter,
  get_post,
  get_posts,
  get_posts_time,
  get_post_no,
  split_file
)


@route('/posts')
def route_posts():
  '''Returns a JSON dictionary about current posts'''
  posts = get_posts_time()
  logging.error(posts)
  posts = [get_post_front_matter(post.get('path'), overwrite=True) for post in posts]

  return {
    'posts': [{
        'time': x.get('time'),
        'last_modified': x.get('time'),
        'title': x.get('title')
      } for x in posts
    ]}
 

@route('/posts/md/:post_id')
def route_post_md(post_id=None):
  return markdown.markdown(split_file(get_post_no(post_id))[1])


@route('/posts/plain/:post_id')
def route_post(post_id=None):
  return {'post': get_post_no(post_id)}

run(server='gae')
