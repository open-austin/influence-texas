nstall
=======

Setup Virtual Environment
.........................

This repository was created with the following::

   $ pyenv install 3.6.1
   $ pyenv virtualenv 3.6.1 influencetx

Note that this repo includes a `.python-version` file that points to `influencetx`. pyenv
will automatically switch to the `influencetx` virtualenv.

Install dependencies
....................

Install dependencies from requirements files::

   $ pip install -r requirements/local.py

Install postgres (for macos)::

   $ brew install postgres@9.6
   $ brew services start postgresql

Install postgres (for debian/ubuntu)::

   $ apt-get install postgresql-9.6

Set up database::

   $ createdb influencetx
   $ python manage.py migrate


Verify installation
...................

Execute tests to verify installation::

   $ py.test

Then, verify that you can start the application server::

   $ python manage.py runserver
