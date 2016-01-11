
#### name:install ####
# download web2py
LinuxOperatingSystem <- function(){
    if(length(grep('linux',sessionInfo()[[1]]$os)) == 1)
    {
      #print('Linux')
      os <- 'linux' 
      OsLinux <- TRUE
    }else if (length(grep('ming',sessionInfo()[[1]]$os)) == 1)
    {
      #print('Windows')
      os <- 'windows'
      OsLinux <- FALSE
    }else
    {
      # don't know, do more tests
      print('Non linux or windows os detected. Assume linux-alike.')
      os <- 'linux?'
      OsLinux <- TRUE
    }
   
    return (OsLinux)
  }
if(LinuxOperatingSystem){
download.file("http://web2py.com/examples/static/web2py_src.zip", 
              destfile = "~/web2py_src.zip", mode = "wb")
unzip("~/web2py_src.zip")
} else {
download.file("http://web2py.com/examples/static/web2py_win.zip", 
              destfile = "~/web2py_win.zip", mode = "wb")
unzip("~/web2py_win.zip")
}

setwd("~/web2py/applications/")
if(!require(downloader)) install.packages("downloader"); require(downloader)
download("https://github.com/ivanhanigan/data_inventory/archive/master.zip", 
         "temp.zip", mode = "wb")
dir()
unzip("temp.zip")
file.rename("data_inventory-master", "data_inventory")
setwd("~/web2py/")
#dir()
system("python ~/web2py/web2py.py -a xpassword -i 0.0.0.0 -p 8181")
#not working go todir and dbl clik then enter pwrd then browse 
browseURL("http://127.0.0.1:8181/data_inventory")
