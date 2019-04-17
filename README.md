# scrummastr
After pulling  this project from the remote repository, you should see two folders (Angular, Django) and this README file.

Django contains the full source.
To get the slack.com to redirect to the Angular front end. open settings.py and edit "FRONTEND" variable on the last line to the appropriate frontend URL

To deploy for Angular, you need to create a new Angular2 project outside of this git repository. Then copy the files from the Angular directory to the src folder in the new project you just created.
Before building, be sure to open up the src/app/data.service.ts file and change the domain_name variable to the domain::port of your Django backend.
Then build <ng build --prod --aot> to generate your files. You should see them in the dist/<your project name> directory.

Below are all dependencies this project needs to work.

Extra Dependencies
==================

Django
------

Use pip to install these:

* channels
* channels_redis
* Django
* django-cors-headers
* djangorestframework
* djangorestframework-jwt
* mysql-connector-python
* slackclient

Angular
-------

Use npm to install these:

* ng2-dragula
* materialize-css

Follow further instructions for materialize-css here:
https://materializecss.com/getting-started.html



