Dropblog: Dropbox Blogging for App Engine
=========================================

(*note*: into ripped from [my blog](http://mvv.io/posts/1))

Dropblog is a tiny [Dropbox][dropbox] CMS I wrote while recovering from pneumonia. 
It runs on top of [App Engine][appengine].  It's inspired by [Jekyll][jekyll], 
but isn't statically generated.

It reads [YAML](http://yaml.org)-compliant metadata, parses markdown posts, 
has a built-in [JSON](http://json.org) API, and is generally pretty badass.


What's more, it's hosted entirely from your [Dropbox][dropbox] folder! 

Just copy over posts and static content to [Dropbox][dropbox] and relax. 
Your changes will automatically deploy.

Remember the days when writing this sort of CRUD meant implementing [a heavyweight 
RDBMS solution](http://wordpress.com)?  What the hell were we smoking?

Plain text and flat files keep things simple, stupid.  The very unix foundation
we stand on has plain text publishing firmly in its roots. From [Kerika's 
blog](http://blog.kerika.com/?p=197):

> Typesetting is closely tied to the history of Unix, and, indeed, provided 
> the raison d’etre for Unix’s existence.  In 1971, when Ken Thompson and 
> Dennis Ritchie (and others) at Bell Labs wanted to get funding for developing 
> the Unix operating system, their business case was based upon the rather 
> tenuous argument that developing this new operating system (Unix) would help 
> them develop a better typesetting program (troff), which could be used by 
> Bell Labs to file patents.

If it's good enough for Ken and Dennis then it's good enough for me.

Features
--------
- Posts and content hosted from your [Dropbox][dropbox] folder!
- [JSON][json] API
- Content is [memcached][memcached]

Setup
-----

### Step One: Setup app key

:warning: **This step is temporary and will be replaced!** 

    $ python dropbox_client.py
    Welcome to the dropblog configuration tool
    Please go to https://www.dropbox.com/1/oauth/authorize?oauth_token=9te9aoa2b4r85kl
    OK ?
    done

### Step Two: Configure App Engine

First register a new app engine app instance.

Next, Change the `application` field in `app.yaml` to your app identifier.

   application: s~yourapphere

**Note**: The `s~` implies a High Replication instance.

### Step Three

Deploy via appcfg

    $ appcfg.py udpate .

### Step Four: Configure Dropbox

Relax!

You're ready to start your dropbox blog.

Read the following [guide](guide_goes_here) to get started.

Notes
-----

`overwrite` query parameter will flush the cache.

Links
-----
- [my blog](http://mvv.io) (powered by dropblog)

[appengine]: https://appengine.google.com/
[memcached]: http://memcached.org/
[dropbox]: http://db.tt/iEMAoeTW
[json]: http://json.org
[jekyll]: http://jekyllrb.com/

License
-------
Dropblog is MIT licensed.

