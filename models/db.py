# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    ## db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
    db = DAL("postgres://w2p_user:xpassword@localhost:5432/data_inventory2")
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] # if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
#### projects

db.define_table(
    'project',
    Field('title', 'string', comment='Suggested structure is: [umbrella project] [data type] [geographic coverage] [temporal coverage]'),
    Field('personnel','string'),
    Field('abstract', 'text')
    )
#### ONE (project) TO MANY (dataset)

db.define_table(
    'dataset',
    Field('project_id',db.project),
    Field('title','string', comment='Suggested structure is: [umbrella project] [data type] [geographic coverage] [temporal coverage]'),
    Field('creator','string', comment='The name of the person, organization, or position who created the data'),
    Field('abstract','string'),
    Field('intellectualrights','string'),
    Field('contact','string'),
    Field('pubdate','date'),
    Field('geographicdescription','string'),
    Field('boundingcoordinates','string'),
    Field('temporalcoverage','string'),
    Field('metadataprovider','string'),
    format = '%(title)s'
    )

db.dataset.contact.requires = [IS_EMAIL()]
  
# db.dataset.metadataprovider.requires = [IS_EMAIL(), IS_NOT_IN_DB(db, 'dataset.metadataprovider')]
#### ONE (dataset) TO MANY (datatables)

db.define_table(
    'datatable',
    Field('dataset_id',db.dataset),
    Field('entityname','string'),
    Field('entitydescription', 'text')
    )
#### ONE (datatable) TO MANY (attributes/variables)

db.define_table(
    'attributelist',
    Field('datatable_id',db.datatable),
    Field('name','string'),
    Field('definition', 'string')
    )
#### accessors

db.define_table(
    'accessor',
    Field('name'),
    Field('email'),
    format = '%(email)s'
    )

db.accessor.name.requires = IS_NOT_EMPTY()
db.accessor.email.requires = [IS_EMAIL(), IS_NOT_IN_DB(db, 'accessor.email')]
#### MANY (datasets) TO MANY (accessors)

db.define_table(
    'accessrequest',
    Field('dataset_id',db.dataset),
    Field('accessor_id',db.accessor),
    Field('title', 'string'),
    format = '%(title)s %(accessor_id)s -> %(dataset_id)s'
    )
#### MANY (keywords) TO one (dataset)

db.define_table(
    'keyword',
    Field('dataset_id',db.dataset),
    Field('thesaurus', 'string', comment = 'source of authoritative definitions'),
    Field('keyword', 'string')
    )
