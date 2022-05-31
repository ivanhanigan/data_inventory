#require("RSQLite")
#drv <- dbDriver("SQLite")
#tfile <- tempfile()
#con <- dbConnect(drv, dbname = "~/tools/web2py/applications/data_inventory_ltern/databases/storage.sqlite")
#dbListTables(con)
#character(0)
require(swishdbtools)
get_passwordTable()
con <- connect2postgres2("data_inventory_ltern_dev_3")
pgListTables(con, "public")

dbGetQuery(con, "select * from project")

ch <- connect2postgres2("ltern")
pgListTables(ch, "ltern")

proj <- dbGetQuery(ch,
                  "
select pn_code_broad_group as title, plot_leader as personnel
FROM ltern.data_deed INNER JOIN ltern.plot_network_code ON ltern.data_deed.pn_deed_code = ltern.plot_network_code.pn_deed_code
GROUP BY pn_code_broad_group, plot_leader, broad_group_ordered
HAVING (((ltern.data_deed.plot_leader) Not Like '%Papst%'))
order by broad_group_ordered
                  ")
proj

proj$abstract <- ""
proj$studyareadescription <- ""
# dbWriteTable(con, name = "project", value = proj, append = T)

for(i in c(1:3,5:12)){
  #i = 4
  pl <- proj[i,"title"]
  print(pl)



dsts <- dbGetQuery(ch,
#cat(
paste("
  SELECT ltern.plot_network_code.pn_code_broad_group,
ltern.data_package.refid,
ltern.data_package.data_package,
ltern.data_package.data_package_title AS title,
ltern.data_package.data_package_type,
ltern.data_package.contact_name AS contact,
ltern.data_package.principal_investigator AS creator,
'' AS abstract,
ltern.data_package.licence_code_package AS intellectualrights,
'' AS pubdate,
ltern.data_package.spatial_resolution AS geographicdescription, ltern.data_package.geographic_description AS boundingcoordinates,
ltern.data_package.temporal_coverage AS temporalcoverage,
'' AS metadataprovider,
ltern.data_package.contract_type as additionalinfo,
ltern.data_package.ltern_publ_url
FROM ltern.data_package INNER JOIN ltern.plot_network_code
ON ltern.data_package.plot_network_study_name = ltern.plot_network_code.plot_network_study_name
WHERE ltern.plot_network_code.pn_code_broad_group = '",pl,"'
 AND (ltern.data_package.tern_type Like 'Project%' OR ltern.data_package.tern_type='Background')
 AND ltern.data_package.availability='Available'
order by ltern.data_package.data_package_title
",sep = "")
)

#head(dsts)
#t(dsts[1,])
#table(dsts$tern_contract_type)
dsts  <- dsts[which(dsts$refid == 105),]
dbWriteTable(con, name = paste("dataset",i,sep=""), value = dsts, append = F)

dbSendQuery(con,
            #cat(
paste("
insert into dataset (project_id, id, shortname, title, keyword, contact, creator, abstract,   geographicdescription, boundingcoordinates, temporalcoverage, metadataprovider, additionalinfo, alternateidentifier)
select ",i,", refid, data_package, title, data_package_type, contact, creator, abstract,   geographicdescription, boundingcoordinates, temporalcoverage, metadataprovider, additionalinfo, ltern_publ_url
from dataset",i,sep ="")
)
dbRemoveTable(con, name = paste("dataset",i,sep=""))

}

# qc
dbGetQuery(con,
           "select tern_contract_type, count(*)
           from dataset
           group by tern_contract_type"
           )
