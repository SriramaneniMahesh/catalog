# Item Catalog Web App Project

BY MAHESH SRIRAMANENI

This web app is a project for the Udacity [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Project overview
This project shows the webapp it allows only user who created the data to edit/delete and add details.If a new user logged in he cannot edit/delete/add other users data but he can view.A new user can add a new bank and he can enter data there his data cannot be edit/delete/add data by other users.

## Skills Required
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6. DataBaseModel

## Files Contain folder
This project contains the files:
main.py
setup_file.py
data_init.py
images folder contains output images
templates folder contains html files
static folder contains css files
client_secrets.json file.

## How to run ItemCatalog Project

Install Vagrant & VirtualBox
- Create Vagrant file `vagrant init ubuntu/xenial64`
- Connect to VirtualMachine `vagrant up`
- Login to VirtualMachine `vagrant ssh`
- Exit from current directory  `cd ..`
- Again exit directory `cd ..`
- Change directory path `cd vagrant`
- Change Project directory `cd catalog`
- To see list of files `ls -l`

## In This Project Main files 

- In this project contains `main.py` contains routes and json endpoints.
- `setup_file.py` contains the database models and tablenames it creates a database file with table.
- `data_init.py` contains the sample data and insert into the database.

### we need to install some modules and python

- Update `sudo apt-get update`
- Install Python `sudo apt-get install python`
- Install pip `sudo apt-get install python-pip`
- Import module `pip install flask`
- Import module`pip install sqlalchemy`
- Import module `pip install oauth2client`
- Import module `pip install httplib2`
- After installing modules we have to run `python setup_file.py` to create database models 
- Next run `python data_init.py` to insert sample data.
- Next run `python main.py` to execute project

							
##Creating API and OAuth client-id 
we have to create a new API and client-id.
To create client id : (https://console.developers.google.com)
- goto to credentials
- create credentials
- Click API KEY
- to create client id we have to create oAuth constent screen
- create OAuth client ID
- Application type(web application)
- Enter name(BankSite)
- Authorized JavaScript origins (http://localhost:8000)
- Authorized redirect URIs = (http://localhost:8000/login) && (http://localhost:8000/gconnect)
- create
- download client_data.json and place it in the folder 


## JSON Endpoints

The following are to check JSON endpoints:

allBanksJSON: `/BankSite/JSON`
    - Displays the whole banks and customer details

categoriesJSON: '/BankSite/bank_Name/JSON'
    - Displays the bank names and its id
	
detailsJSON: '/BankSite/banks/JSON'
	- It displays all customer details in banks

categorydetailsJSON: '/BankSite/<path:bankname>/banks/JSON'
    - It displays the details in a particular bank

DetailsJSON:
'/BankSite/<path:bankname>/<path:cusdetails_name>/JSON'
    - It displays the details that the bank name and cus_name matches

## Final output images:

![home.png](https://github.com/SriramaneniMahesh/catalog/blob/master/images/home.png)
![login.png](https://github.com/SriramaneniMahesh/catalog/blob/master/images/login.png)
![loginuser.png](https://github.com/SriramaneniMahesh/catalog/blob/master/images/loginuser.png)
![logsuccess.png](https://github.com/SriramaneniMahesh/catalog/blob/master/images/logsuccess.png)
![addcat.png](https://github.com/SriramaneniMahesh/catalog/blob/master/images/addcat.png)
![additem.png](https://github.com/SriramaneniMahesh/catalog/blob/master/images/additem.png)
![edit.png](https://github.com/SriramaneniMahesh/catalog/blob/master/images/edit.png)
![delete.png](https://github.com/SriramaneniMahesh/catalog/blob/master/images/delete.png)
![json.png](https://github.com/SriramaneniMahesh/catalog/blob/master/images/json.png)
![logout.png](https://github.com/SriramaneniMahesh/catalog/blob/master/images/logout.png)
