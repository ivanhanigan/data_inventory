
response.menu = [['Inventory Home', False, URL('data_inventory','default','index')],
                 ['Manage Projects', False, URL('manage_projects')],
                 ['Manage Datasets', False, URL('manage_datasets')],
                 ['Manage Accessors or Groups', False, URL('manage_accessors_or_groups')],
                 ['Set Access to a Dataset', False, URL('access_dataset')],
                 ['Documentation', False, XML(URL('static','index.html', scheme=True, host=True))]]
def access_dataset():
    form = SQLFORM.factory(
        Field('accessdataset_id',requires=IS_IN_DB(db,db.accessdataset.id,'%(name)s')),
        Field('dataset_id',requires=IS_IN_DB(db,db.dataset.id,'%(shortname)s')),
        Field('title','string',requires=IS_NOT_EMPTY()),
        Field('description','text',requires=IS_NOT_EMPTY()),
        Field('begin_date','date'),
        Field('end_date','date')).process()

    
    if form.accepted:
        # get previous access for same dataset
        access = db((db.accessrequest.accessdataset_id == form.vars.accessdataset_id)&
            (db.accessrequest.dataset_id==form.vars.dataset_id)).select().first()

        db.accessrequest.insert(accessdataset_id=form.vars.accessdataset_id,
                         dataset_id=form.vars.dataset_id,
                         title=form.vars.title,
                         description=form.vars.description,
                         begin_date =form.vars.begin_date,
                         end_date   =form.vars.end_date
                         )

        response.flash = 'dataset accessed!'
    elif form.errors:
        response.flash = 'invalid values in form!'

    
    # now get a list of all accesses
    accessing = (db.accessdataset.id==db.accessrequest.accessdataset_id)&(db.dataset.id==db.accessrequest.dataset_id)
    records = SQLTABLE(db(accessing).select(),headers='fieldname:capitalize')
    return dict(form=form, records=records)
def manage_projects():
    grid = SQLFORM.smartgrid(db.project,linked_tables=['dataset', 'entity', 'keyword', 'intellectualright', 'attr','accessrequest'
                                                      ],
                             fields = [db.project.title,db.project.id,db.project.personnel_data_owner,
                                       db.dataset.shortname,
                                       db.dataset.id,
                                       db.dataset.shortname,
                                       db.dataset.creator,                                          
                                       db.dataset.contact,
                                       db.entity.entityname, db.entity.physical_distribution,
                                       db.attr.variable_name, db.attr.variable_definition,
                                       db.accessrequest.accessdataset_id, 
                                       db.accessrequest.dataset_id,
                                       db.accessrequest.title, 
                                       db.keyword.keyword,
                                       db.intellectualright.licence_code],
                                       orderby = dict(project=db.project.id, dataset=db.dataset.title),
                             user_signature=True,maxtextlength =200)
    return dict(grid=grid)
def manage_datasets():
    grid = SQLFORM.smartgrid(db.dataset,linked_tables=['project', 'entity','keyword', 'intellectualright', 'attr','accessrequest'
                                                      ],
                             fields = [db.project.title,db.project.id,db.project.personnel_data_owner,
                                       db.dataset.shortname,
                                       db.dataset.id,
                                       db.dataset.shortname,
                                       db.dataset.creator,                                          
                                       db.dataset.contact,
                                       db.entity.entityname, db.entity.physical_distribution,
                                       db.attr.variable_name, db.attr.variable_definition,
                                       db.accessrequest.accessdataset_id, 
                                       db.accessrequest.dataset_id,
                                       db.accessrequest.title, 
                                       db.keyword.keyword,
                                       db.intellectualright.licence_code],
                             user_signature=True,maxtextlength =200)
    return dict(grid=grid)
def manage_accessors_or_groups():
    grid = SQLFORM.smartgrid(db.accessdataset,linked_tables=['accessor'],
                             fields = [
                                       db.accessdataset.name,
                                       db.accessdataset.email,
                                       db.accessor.name, db.accessor.email],
                                       orderby = dict(accessdataset=[db.accessdataset.name]),
                             user_signature=True,maxtextlength =200)

    return dict(grid=grid)
    # db.accessor.email.requires = [IS_IN_DB(db,db.accessor.id,'%(email)s')]
def manage_crosswalk():
    grid = SQLFORM.smartgrid(db.crosswalk,
                             fields = [db.crosswalk.transfer2new,   
                                       db.crosswalk.eml_node,
                                       db.crosswalk.datinv,
                                       db.crosswalk.ltern_name,
                                       db.crosswalk.portal_ddf_qaf,
                                       db.crosswalk.ddi_node,
                                       db.crosswalk.aekos_shared
                                       ],
                                       orderby = dict(crosswalk=[db.crosswalk.transfer2new, db.crosswalk.portal_ddf_qaf, db.crosswalk.eml_node]),
                             user_signature=True,maxtextlength =200)

    return dict(grid=grid)
def manage_thesaurus_ltern():
    grid = SQLFORM.smartgrid(db.thesaurus_ltern,
                             fields = [   
                                       db.thesaurus_ltern.keyword
                                       ],
                                       orderby = dict(thesaurus_ltern=[ db.thesaurus_ltern.keyword]),
                             user_signature=True,maxtextlength =200)

    return dict(grid=grid)
