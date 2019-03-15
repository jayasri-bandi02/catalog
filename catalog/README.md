# Item Catalog Web Application
Full Stack Nano degree Udacity Project-Item Catalog 
----Done By--Bandi Jaya Sri

## What to do ?
The project is to develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users can perform CRUD operations on the items and categories.

## About
This project is a a RESTful web application using the Python framework Flask along with implementing third-party OAuth authentication. We will use various HTTP methods available related to CRUD (create, read, update and delete) operations ,with the help of postgresql database that stores various ice cream falvour names and their items. OAuth2 provides authentication for further CRUD functionality on the application.  OAuth2 is implemented for Google Accounts currently.

## In This Project
->This project has one main Python module `main.py` which runs the Flask application. 
->A database named 'items' is created with tables and their columns by running a python module 'Data_Setup.py'.
->Initially,data is entered into tables with a minimum no.of categories and an item in it by running 'database_init.py'
->The Flask application uses stored HTML templates in which the folder is used  to build the front-end of the application.
->The images folder contains the screenshots of different web pages while performing operations .
->The json_output folder contains the screenshots of the data retrieved while running the json links.
->All the python files are neatly formatted with 'pep8' style guide ...results are placed
in the pep8 check folder.
## Skills Required
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6.DataBaseModels

## Required Tools
1. Python
2. Vagrant
3. VirtualBox

## Installation
There are some dependancies and a few instructions on how to run the application.
Seperate instructions are provided to get GConnect working also.

## Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## How to Install
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repository or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd /vagrant` as instructed in terminal
6. Setup application database `python Data_Setup.py`
7. Insert sample data `python database_init.py`
8. Run application using `python  main.py`


Optional steps:

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'CreamyCorner'
7. Authorized JavaScript origins = 'http://localhost:4444'
8. Authorized redirect URIs = 'http://localhost:4444/login' && 'htttp://localhost:4444/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in  the working directory .
14. Run application using `python main.py`

##How to run
1.Launch the Vagrant VM (vagrant up)
2.The Flask application written locally in the vagrant/Item_Catalog directory  will be automatically  synced to /vagrant/Item_Catalog within the VM).
3.Run your application within the VM (python /vagrant/Item_Catalog/main.py)
Access and test your application by visiting http://localhost:4444 locally

##Output
The sample project display is as follows in the web browser..
Running the application..(http://localhost:4444) 
-->All the screenshots or the sample display of web pages are placed in the 'images' folder in the project folder with respective names.
-->Similarly,The screenshots of output by running the json links are placed in the 'json_output' folder.

## Miscellaneous
This project is inspiration from [gmawji](https://github.com/gmawji/item-catalog).
