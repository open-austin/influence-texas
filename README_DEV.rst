influencetx
===========

`influencetx`: An `ATX Hack for Change`_ project for accessing Texas campaign finance and voting
records.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


.. _ATX Hack for Change: http://atxhackforchange.org/


Setup
-----

To get started on this project for the first time, you can follow these simple steps.

- `Install Docker CE`_
- Clone code::

      cd your/code/directory
      git clone https://github.com/open-austin/influence-texas.git

- Start up docker container::

      cd influence-texas
      docker-compose up -d

The first time it's run `docker-compose` will pull down generic python and postgres images. After
that, it will install dependendencies specific to the app and start up a server for the
`influencetx` app at http://localhost:8000/.

.. _Install Docker CE: https://docs.docker.com/engine/installation/

Add Open States API Key
.......................

If you want to use portions of the site that rely on the Open States API, you'll need to add an
API key to the secrets file.

- `Register for an Open States API key`_

  - Use your own name and email
  - Website: ``https://www.open-austin.org/``
  - Organization: ``Open Austin``
  - Intended Usage: ``Local development of influencetx app``

- You should receive an email with your new API key. Follow the activation link.
- Copy your api key into the following command and run it in the root directory of the repo (i.e. where README.md is located)::

    echo "OPENSTATES_API_KEY=YOUR-API-KEY-HERE" >> .influencetx-secrets.env

Note that **changes to .influencetx-secrets.env should never be committed**.

.. _Register for an Open States API key: https://openstates.org/api/register/

Basic Commands
--------------

During everyday development, there are a few commands that you'll need to execute to debug, update
the database, etc. All of the basic commands are based off of the following commands for
interacting with the docker container:

- `docker-compose`_: Run generic docker commands in docker containers.

  - Run ``docker-compose -h`` to see a full list of commands.
  - Run ``docker-compose help <COMMAND>`` to see help on a command.

- ``./pyinvoke.sh``: A shortcut for running invoke_ commands in docker containers.

  - Run ``./pyinvoke.sh -l`` to see a full list of commands.
  - Run ``./pyinvoke.sh -h <COMMAND>`` to see help on a command.

- ``./djadmin.sh``: A shortcut for running `django admin`_ commands in docker containers.

  - Run ``./djadmin.sh help`` to see a full list of commands.
  - Run ``./djadmin.sh help <COMMAND>`` to see help on a command.

These instructions assume you're executing the command from the parent directory of this file. You
can find details of any commands using the commands above. A few commonly used commands are

.. _docker-compose: https://docs.docker.com/compose/reference/
.. _invoke: http://www.pyinvoke.org/
.. _django admin: https://docs.djangoproject.com/en/1.11/ref/django-admin/


Maintenance commands
....................

The commands commonly used for maintenance of this project are described below.

- ``docker-compose up -d``: Start up docker container in detached mode (background task). You can
  keep a docker container running continuously, so you may only need to run this after restarting
  your machine.
- ``./djadmin.sh makemigrations``: Make schema migrations to reflect your changes to Django models.
  Any migrations that you make should be committed and pushed with your model changes.
- ``./djadmin.sh migrate``: Migrate database to the current schema. You'll need to run this after
  running ``./djadmin.sh makemigrations`` to actually apply migrations. If you pull code from github
  that includes migrations, you should run this to sync your database.
- ``./pyinvoke.sh test``: Execute tests using pytest. At minimum, run this before committing code.
- ``./pyinvoke.sh check``: Check project for problems. At minimum, run this before committing code.
- ``./pyinvoke.sh create-app``: Create `Django app`_. Django apps are small collections of
  functionality for your web application.

.. _Django app: https://docs.djangoproject.com/en/1.11/ref/applications/#projects-and-applications


Debugging commands
..................

- ``docker-compose logs --follow``: Watch output of containers. (Alias: ``-f`` = ``--follow``.)
- ``docker-compose logs``: Display bash output for all containers.
- ``docker-compose exec web bash``: Run bash shell within web container.
- ``./djadmin.sh shell``: Start IPython shell.
- ``./djadmin.sh dbshell``: Start Postgres shell.


Debugging Python code
.....................

You can't use the output window from a ``docker-compose logs --f`` call to debug, since it actually
interacts with multiple containers. Instead, run the following in a terminal::

    docker attach `docker-compose ps -q web`

This will attach the terminal to the web container and allow you to interact with the running
process. Now you can add a break point somewhere in your python code::

    import ipdb; ipdb.set_trace()


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html
