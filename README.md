# The Social Network

A Web Programming and DB project based on Flask, jinja2, Mysql/Postgresql, jQuery, HTML, and CSS + Bootstrap.

Functionalities currently implemented are:
  - Register and Login to an account
  - Post text-posts, or image-links to load images
  - Like posts made by other users
  - Follow an user to see their posts on a custom wall
  - Comment on posts made by anyone
  - Be able to delete/edit your posts/profile on the go
  
  
### Tech
 
The Social Network uses a number of Frameworks and Languages to work properly:

* Flask - Python Miniframework to make and deploy web apps
* WTForms - Python Module for an Object Oriented implementation of Forms
* Visual Studio - An awesome text editor by Microsoft
* Bootstrap - Template for pretty css
* Jinja2 - HTML templating engine
* FontAwesome - Amazing fonts by Google
* jQuery - Javascript framework to automate client side scripting
* psycopg2 - Python Module to work with PostgreSQL

### Installation

The Social Network requires [Python 3.7.2](https://www.python.org/downloads/) to run.

If you wish to run the app locally you can clone from the [repository](https://github.com/DevangJ/theSocialNetwork)
```sh
$ git clone https://github.com/DevangJ/theSocialNetwork
```

Create the postgreSQL database from the given dump

```sh
$ cd theSocialNetwork
$ psql thesocialnetwork < new.dump
```

Set up the virtual environment, install the dependencies and start the server.

```sh
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python app.py
```

Your instance of the app will be running on
> 0.0.0.0:8000/
