
#### Data Inventory


## About

1. A web2py app to help manage research data
1. Designed for the Ecology discipline, using Ecological Metadata Language standard concepts
1. Can run as simple standalone desktop app using sqlite or shared on a postgres server for concurrent access by a team
1. Highly customised for the Oz Long Term Ecological Research Network Data Portal's needs


### To install

1. Download the 2.x version web2py binaries http://www.web2py.com/init/default/download and unzip
1. Put all the files into your web2py/applications as 'data_inventory' or the name you want
1. Dbl-Click to Run the wep2py.py file and go to 127.0.0.1:8000/data_inventory
1. In the top right corner you have to sign up first with a local username and password
1. README is at http://127.0.0.1:8181/data_inventory/static/index.html

### Roadmap for python3

1. investigate port to py4web (the evolution of web2py: https://github.com/web2py/py4web)
2. for the time being try to continue using with python 2. 
3. if using the postgres database backend need to use older psycopg2 (to avoid postgres `RuntimeError: No driver of supported ones ('psycopg2',) is available`)

```
sudo apt update
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
sudo python2 get-pip.py
pip2 install psycopg2-binary
```

Licence: CC-BY-4.0

![cc-by-4_0.png](cc-by-4_0.png)
