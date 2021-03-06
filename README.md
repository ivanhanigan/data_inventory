
#### Data Inventory


## About

1. A web2py app to help manage research data
1. Designed for the Ecology discipline, using Ecological Metadata Language standard concepts
1. Can run as simple standalone desktop app using sqlite or shared on a postgres server for concurrent access by a team
1. Highly customised for the Oz Long Term Ecological Research Network Data Portal's needs

## To install using R:

```{r}
setwd("~")
if(!require(downloader)) install.packages("downloader"); require(downloader)
download("https://raw.githubusercontent.com/ivanhanigan/data_inventory/master/static/install.R",
         "install.R", mode = "wb")
source("install.R")
# this downloads the required software and database, but you need to start it manually
# go to web2py/ and click web2py.exe under windoze, or just bash it in linux.
# installer features are on my TODO list, thanks for your patience.
```

### or alternatively do a manual install

1. Download web2py http://www.web2py.com/init/default/download 
1. Put all the files into your web2py/applications as 'data_inventory'
1. Dbl-Click to Run the wep2py.py file and go to 127.0.0.1:8000/data_inventory
1. README is at http://127.0.0.1:8181/data_inventory/static/index.html

Licence: CC-BY-4.0

![cc-by-4_0.png](cc-by-4_0.png)
