This is a flask template application to enable a user to quickly setup a flask application

Install the dependencies and devDependencies and start the server.

```sh
$ git clone the project
$ python3 venv venv //create virtual environment
$ source venv/bin/activate //start the virtual environment on windows ./venv/bin/activate.bat
$ pip install -r requirements.txt
```
generate python secret
```sh
$ python //command to start python in the command shell
$ import secrets
$ secrets.token_urlsafe(16) //this will generate a secret key which you can copy and past in .env file
$ exit() // to exit from shell command
```

used to create a database migration

```sh
$ flask db init
$ flask db migrate
$ flask db upgrate
```

run flask ...

```sh
$ flask run

```
 - managing dependancies the project uses `pip-compile` for further reading https://suyojtamrakar.medium.com/managing-your-requirements-txt-with-pip-tools-in-python-8d07d9dfa464 or https://pypi.org/project/pip-tools/
 - most of the api logic is done within the app file, while the tests are created on tests folder which has a helper file which can be used
   for mocking api calls
 - included also has an example files which can be used to create a dockerfile, bitbucket-piplelines,


# Poetry
 - this is a python dependancy manager which has been installed on this project
 - To install poetry in your system follow instructions from https://python-poetry.org/docs/


# Docker
To run the project using docker

this will start the docker image but will build the image first
```sh
  $ docker-compose up --build
```

once built you can simply run
```sh
  $ docker-compose up
```
