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
    ##db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
    db = DAL("postgres://w2p_user:xpassword@localhost:5432/data_inventory_hanigan_dev")
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
Field('title', 'string',
comment= XML(T('The EML Project module places the data into its larger research context. Suggested structure is: [Plot Network] OR [geographic coverage] [data type]. %s',
A('More', _href=XML(URL('static','index.html',  anchor='sec-5-1-1', scheme=True, host=True)))))
),
Field('personnel','string', 
comment= XML(T('Compulsory. A project must have at least one originator. At LTERN this is assumed to have role = data owner unless different role is specified. %s',
A('More', _href=XML(URL('static','index.html',  anchor='sec-5-1-2', scheme=True, host=True)))))
),
Field('abstract', 'text',
comment= XML(T('Descriptive abstract that summarizes information about the umbrella project context of the specific project. %s',
A('More', _href=XML(URL('static','index.html',  anchor='sec-5-1-3', scheme=True, host=True)))))
),
Field('studyAreaDescription','string', 
comment= XML(T('This can include descriptions of the geographic, temporal, and taxonomic coverage of the research location. %s', 
A('More', _href=XML(URL('static','index.html', anchor='sec-5-1-4', scheme=True, host=True)))))
),
format = '%(title)s' 
)
  
db.project.personnel.requires = IS_NOT_EMPTY()
#### ONE (project) TO MANY (dataset)

db.define_table(
    'dataset',
    Field('project_id',db.project),
    Field('shortname','string', comment = XML(T('A concise name that describes the resource that is being documented. Example is vernal-data-1999. %s.',
    A('More', _href=XML(URL('static','index.html',  anchor='sec-5-2', scheme=True, host=True)))))
    ),
    Field('title','text', comment='Suggested structure is: [umbrella project] [data type] [geographic coverage] [temporal coverage]'),
    Field('keyword','string',
    comment = XML(T('A single keyword or key phrase that concisely describes the resource. Example is biodiversity. More can be added via the keywords table. %s.',
    A('More', _href=XML(URL('static','index.html',  anchor='sec-5-2', scheme=True, host=True)))))
    ),
    Field('contact','string', comment = 'An email address for general enquiries.  This field is compulsory.'),
    Field('creator','string', comment='The name of the person, organization, or position who created the data'),
    Field('alternateidentifier','string',
    comment = XML(T('Additional identifier that is used to label this dataset. %s.',
    A('More', _href=XML(URL('static','index.html',  anchor='sec-5-2', scheme=True, host=True)))))     
    ),
    Field('abstract','text'),
    Field('pubdate','date'),
    Field('geographicdescription','string'),
    Field('boundingcoordinates','string'),
    Field('temporalcoverage','string'),
    Field('metadataprovider','string'),
    Field('additionalinfo','string', comment = XML(T('Any information that is not characterised well by EML metadata. Example is a group id for grouping datasets apart from EML-project. %s.',
  A('More', _href=XML(URL('static','index.html',  anchor='sec-5-2', scheme=True, host=True)))))
    ),
    format = '%(shortname)s'
    )

db.dataset.contact.requires = [IS_EMAIL()]

    
# db.dataset.metadataprovider.requires = [IS_EMAIL(), IS_NOT_IN_DB(db, 'dataset.metadataprovider')]
#### ONE (dataset) TO MANY (entity)

db.define_table(
    'entity',
Field('dataset_id',db.dataset),
Field('entityname','string'),
Field('entitydescription', 'text'),
Field('physical_distribution', 'string',
comment= XML(T('Information required for retrieving the resource. %s',    
  A('More', _href=XML(URL('static','index.html',  anchor='sec-5-3-4', scheme=True, host=True)))))
  ),
Field('numberOfRecords', 'integer'),
format = '%(entityname)s'
)
#### ONE (entity) TO MANY (attributes/variables)

db.define_table(
    'attr',
    Field('entity_id',db.entity),
    Field('name','string'),
    Field('definition', 'string')
    )
#### accessdatasets

db.define_table(
    'accessdataset',
    Field('name'),
    Field('email'),
    Field('title', 'string'),
    Field('description', 'text'),
    format = '%(name)s'
    )
#       format = '%(email)s'
db.accessdataset.name.requires = IS_NOT_EMPTY()
# db.accessdataset.email.requires = [IS_EMAIL(), IS_NOT_IN_DB(db, 'accessdataset.email')]
#### MANY (accessors) TO MANY (accessdataset members)

db.define_table(
    'accessor',
    Field('accessdataset_id',db.accessdataset),
    Field('name'),
    Field('email'),
    )
db.accessor.email.requires = [IS_EMAIL()]
# , IS_NOT_IN_DB(db, 'accessor.email')]
#### MANY (datasets) TO MANY (accessors)

db.define_table(
    'accessrequest',
    Field('dataset_id',db.dataset),
    Field('accessdataset_id',db.accessdataset),
    Field('title', 'string'),
    format = '%(title)s %(accessdataset_id)s -> %(dataset_id)s'
    )
#### MANY (keywords) TO one (dataset)

db.define_table(
    'keyword',
    Field('dataset_id',db.dataset),
    Field('thesaurus', 'string', comment = 'source of authoritative definitions'),
    Field('keyword', 'string')
    )
#### ONE (intellectualright) TO one (dataset)
db.define_table(
    'intellectualright',
    Field('dataset_id',db.dataset),
    Field('data_owner', 'string'),
    Field('special_permissions', 'string'),
    Field('licence_code', 'string')
    )
    
db.intellectualright.data_owner.requires = IS_NOT_EMPTY()    
db.intellectualright.licence_code.requires = IS_IN_SET(['CCBY', 'TERN-BYNC', 'adhoc'])
#### ONE (checklist) TO one (dataset)
db.define_table(
    'checklist',
    Field('dataset_id',db.dataset),
Field('checked_by','string'),
Field('check_date','date'),
Field('notes_comments','text'),
Field('data_package_title_check','boolean'),
Field('data_set_citation_check','boolean'),
Field('data_package_owner_check','boolean'),
Field('data_package_owner_check_individual_name','boolean'),
Field('data_package_owner_check_position_role','boolean'),
Field('data_package_owner_check_organization','boolean'),
Field('data_package_owner_check_address','boolean'),
Field('data_package_owner_check_phone','boolean'),
Field('data_package_owner_check_email_address','boolean'),
Field('associated_parties','boolean'),
Field('associated_parties_individual_name','boolean'),
Field('associated_parties_position','boolean'),
Field('associated_parties_organization','boolean'),
Field('associated_parties_physical_address','boolean'),
Field('associated_parties_phone','boolean'),
Field('associated_parties_email_address','boolean'),
Field('abstract','boolean'),
Field('keywords_and_subject_categories','boolean'),
Field('gcmd_science_keywords','boolean'),
Field('anzsrc_for_codes','boolean'),
Field('ltern_monitoring_themes','boolean'),
Field('keywords_free_text','boolean'),
Field('geographic_coverage','boolean'),
Field('geographic_description','boolean'),
Field('bounding_coordinates','boolean'),
Field('temporal_coverage','boolean'),
Field('contacts_individual_names','boolean'),
Field('contacts_positions','boolean'),
Field('contacts_organizations','boolean'),
Field('contacts_addresses','boolean'),
Field('contacts_phone','boolean'),
Field('contacts_email_addresses','boolean'),
Field('methods_and_sampling_information','boolean'),
Field('method_step_titles','boolean'),
Field('method_step_description','boolean'),
Field('instrumentation_details','boolean'),
Field('sampling_area_and_frequency','boolean'),
Field('sampling_description','boolean'),
Field('research_project_title','boolean'),
Field('research_project_funding_sources','boolean'),
Field('research_project_personnel_information','boolean'),
Field('research_project_individual_name','boolean'),
Field('research_project_position_role','boolean'),
Field('research_project_organization','boolean'),
Field('research_project_address','boolean'),
Field('research_project_phone','boolean'),
Field('research_project_email_address','boolean'),
Field('research_project_role','boolean'),
Field('additional_metadata','boolean'),

Field('access_control','boolean'),

Field('usage_rights','boolean'),
Field('special_conditions','boolean'),
Field('entity_metadata','boolean'),
Field('homepage_content','boolean'),
Field('eml_homepage_links','boolean'),
Field('can_the_plot_network_or_data_package_be_filtered_in_the_search_bar_of_the_portal','boolean'),
Field('draft_publication_checklist_passed','boolean'),
Field('metacat_publication_checklist_check_public_or_mediated_access','boolean'),
Field('metacat_publication_checklist_add_publication_date_to_data_inventory','boolean'),
Field('metacat_publication_checklist_passed','boolean'),
Field('reporting_checklist_licenced','boolean'),
Field('reporting_checklist_described_with_metadata_','boolean'),
Field('reporting_checklist_doi_minted','boolean'),
Field('reporting_checklist_metadata_feed_to_tddp_and_rda','boolean'),
Field('reporting_checklist_passed','boolean')
    )
    
db.checklist.checked_by.requires = IS_IN_SET(['Claire', 'Karl'])
db.checklist.check_date.requires = IS_NOT_EMPTY()
#### ONE (errors) TO one (dataset)
db.define_table(
    'error',
    Field('dataset_id',db.dataset),
Field('logged_by','string'),
Field('date_logged','date'),
Field('date_actioned','date'),
Field('error','text'),
Field('addenda','text')
    )
    
db.error.logged_by.requires = IS_NOT_EMPTY()
db.error.date_logged.requires = IS_NOT_EMPTY()
db.define_table(
    'crosswalk',
    Field('transfer2new','string'),
    Field('eml_module','string'),
    Field('eml_table','string'),
    Field('eml_node','string'),
    Field('eml_desc','text'),
    Field('eml_standard_link','string'),
    Field('eml_local_link','string'),
    Field('morpho','string'),
    Field('ltern_table','string'),
    Field('ltern_name','string'),
    Field('datinv','string'),
    Field('portal_ddf_qaf','string'),
    Field('help_comment','string'),
    Field('ltern_desc','text'),
    Field('aekos_shared','string'),
    Field('aekos_desc','text'),
    Field('ddi_module','string'),
    Field('ddi_node','string'),
    Field('asn','string'),
    Field('tern','string'),
    Field('ala','string'),
    Field('psql_type','string'),
    Field('w2p_code','string'),
    Field('constraint_text','string'),
    Field('lter_manual_page','string')
    )
