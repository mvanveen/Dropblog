Title:  Todos
Author: Michael Van Veen
Time:   1325214553 

Droptable TODOS
===============

Short Term
==========
- unicode support
- custom url routing
- templates/ directory routing
- app.yaml file
- better testing
  - Updating templates with ?overwrite=True works
  - Updating posts with ?overwrite=True works
- tags

Mid Term
========
- plugins
- handlebars support?
- Jekyll importer
- Wordpress importer?

URL Routing Architecture
------------------------

### High-level

1. Keep a dict of urls which map resource to url

items should look like:
(url, memcache_resource, metadata)

metadata includes things like:
  - title
  - time/date
  - template/post

2. Items 

