
######################################################################################################S
datinv2eml <- function(
    ch = ch
    , 
    proj_name = "Biomass_Smoke_Validated_Events" 
    ,
    dset_shortname = "Biomass_Smoke_Validated_Events"
    ,
    entity_name = "storage.sqlite"
    ,
    show_data_table = FALSE
    ,
    datinv_source = "datinv"
){
  ls_projs <- dbGetQuery(ch, "select title from project")
  ##ls_projs
  # retrieve project metadata
  meta_proj <- as.data.table(
    dbGetQuery(ch, sprintf(
      "select * from project 
    where title = '%s' ", proj_name))
  )
  
  ##meta_proj  

  
  # retrieve datasets metadata
  meta_dataset <- as.data.table(
    dbGetQuery(ch, sprintf(
      "select dataset.* 
      from dataset
      join project on 
      dataset.project_id = project.id
      where project.title = '%s' ", proj_name))
  )
  ##meta_dataset[,1:5]
  meta_dataset <- meta_dataset[shortname == dset_shortname,]
  ##meta_dataset$geographicdescription
  bbox1 <- strsplit(meta_dataset$boundingcoordinates,split = ",")
  bbox <- lapply(bbox1, strsplit, ":")
  bbox <- t(rbindlist(bbox))
  bbox <- gsub(" ","",bbox)
  ##bbox[which(bbox[,1]=="north"),2]
  coverage <- set_coverage(geographicDescription = meta_dataset$geographicdescription,
                           north = bbox[which(bbox[,1]=="north"),2], south = bbox[which(bbox[,1]=="south"),2],
                           east = bbox[which(bbox[,1]=="east"),2], west = bbox[which(bbox[,1]=="west"),2])
  
  meta_rights <- as.data.table(
    dbGetQuery(ch, sprintf(
      "select intellectualright.* from intellectualright
    join dataset on intellectualright.dataset_id = dataset.id
    where dataset.id IN (%s) ", 
      meta_dataset$id
    ))
  )
  #meta_rights
  
  #### start metadata ####
  creator_dat <- strsplit(meta_dataset$creator," ")
  creator_info <- eml$creator(
    individualName = eml$individualName(
      givenName = creator_dat[[1]][1], 
      surName = creator_dat[[1]][2]),
    userId = eml$userId("ORCID")
  )
  
  orcid <- dbGetQuery(ch, paste0("select * from orcid where name_per_creator_tbl = '",creator_dat[[1]][1]," ",creator_dat[[1]][2],"'"))
  ##orcid
  creator_info$userId[[2]] <- paste0("https://orcid.org/", orcid$orcid)
  #creator_info
  
  contact_info <- eml$contact(positionName = meta_dataset$contact,
                              electronicMailAddress = meta_dataset$contact_email)
  #contact_info
  
  entity <- dbGetQuery(ch, paste0("select * from entity where dataset_id = ", meta_dataset$id))
  entity <- entity[entity$entityname == entity_name,]
  #t(entity)
  
  attributes <- dbGetQuery(
    ch,
    paste0(
      'select
variable_name as "attributeName",
variable_definition as "attributeDefinition"
from attr where entity_id = ',
      entity$id
    )
  )
  meta_dataset$pubdate <- ifelse(is.na(meta_dataset$pubdate), Sys.Date(), meta_dataset$pubdate)
  
  #### do the EML ####
  if(show_data_table){ 
  attributes$measurementScale <- "nominal"
  attributes$domain <- "textDomain"
  attributeList <-  set_attributes(attributes)
  my_eml <- eml$eml(
    packageId = uuid::UUIDgenerate(),  
    system = "uuid",
    dataset = eml$dataset(
      id = as.character(paste(datinv_source, meta_dataset$id, sep = "_")),
      shortName = meta_dataset$shortname,
      title = meta_dataset$title,
      creator = creator_info,
      contact = contact_info,
      pubDate = meta_dataset$pubdate,
      abstract = meta_dataset$abstract,
      coverage = coverage,
      intellectualRights = meta_rights$special_conditions,
      publisher = list(organizationName = meta_dataset$publisher),
      alternateIdentifier = meta_dataset$alternate_identifier,
      dataTable = eml$dataTable(
        entityName = entity$entityname,
        entityDescription = entity$entitydescription,
        attributeList = attributeList                                         
      )
      ,
      project = eml$project(id = as.character(meta_proj$id),
                            title = meta_proj$title,
                            personnel = eml$personnel(
                              individualName = list(givenName = strsplit(meta_proj$personnel_data_owner," ")[[1]][1]
                                                    ,
                                                    surName = strsplit(meta_proj$personnel_data_owner," ")[[1]][2]
                              ),
                              organizationName = "Curtin University",
                              role = "principalInvestigator"),
                            
                            abstract = meta_proj$project_abstract,
                            funding = meta_proj$funding
      )
      
    ),
    additionalMetadata = eml$additionalMetadata(metadata = list(unitList = meta_dataset$additional_metadata))
  )
  } else {
    my_eml <- eml$eml(
      packageId = uuid::UUIDgenerate(),  
      system = "uuid",
      dataset = eml$dataset(
        id = as.character(paste(datinv_source, meta_dataset$id, sep = "_")),
        shortName = meta_dataset$shortname,
        title = meta_dataset$title,
        creator = creator_info,
        contact = contact_info,
        pubDate = meta_dataset$pubdate,
        abstract = meta_dataset$abstract,
        coverage = coverage,
        intellectualRights = meta_rights$special_conditions,
        publisher = list(organizationName = meta_dataset$publisher),
        alternateIdentifier = meta_dataset$alternate_identifier
        
        ,
        project = eml$project(id = as.character(meta_proj$id),
                              title = meta_proj$title,
                              personnel = eml$personnel(
                                individualName = list(givenName = strsplit(meta_proj$personnel_data_owner," ")[[1]][1]
                                                      ,
                                                      surName = strsplit(meta_proj$personnel_data_owner," ")[[1]][2]
                                ),
                                organizationName = "Curtin University",
                                role = "principalInvestigator"),
                              
                              abstract = meta_proj$project_abstract,
                              funding = meta_proj$funding
        )
        
      ),
      additionalMetadata = eml$additionalMetadata(metadata = list(unitList = meta_dataset$additional_metadata))
    )
  }
  emld::eml_version("eml-2.1.1")
  return(my_eml)
}

#########################################################################################3
