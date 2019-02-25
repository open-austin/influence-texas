===========
influencetx
===========

`influencetx`: An `ATX Hack for Change`_ project for accessing Texas campaign finance and voting
records.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


.. _ATX Hack for Change: http://atxhackforchange.org/


Setup
=====


To get started on this project for the first time, you can follow these simple steps.

- `Install Docker CE`_
- Clone code::

      cd your/code/directory
      git clone https://github.com/open-austin/influence-texas.git
      cd influence-texas

- Define environment variables (see below) and export those variables::

      source env.sh

- Start up docker container::

      docker-compose up -d

The first time it's run, `docker-compose` will pull down generic python and postgres images. After
that, it will install dependendencies specific to the app and start up a server for the
`influencetx` app at http://localhost:5120/.

.. _Install Docker CE: https://docs.docker.com/engine/installation/

Define environment variables
----------------------------

Credentials are stored as environment variables that are not committed to source control. To make
your environment reproducible, you'll add these environment variables to a script named ``env.sh``
with the following values::

    export OPENSTATES_API_KEY=YOUR-API-KEY
    export TPJ_DB_USER=YOUR-USERNAME
    export TPJ_DB_PASSWORD=YOUR-PASSWORD

The TPJ variables require credentials from Texans for Public Justice. Currently, there's no
established process for acquiring those credentials. See the following section to acquire an
OpenStates key.

When you start up a new shell, you should run the following to setup environment variables::

    source env.sh

Note that **changes to env.sh should never be committed**.

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
- Copy key to ``env.sh``.

.. _Register for an Open States API key: https://openstates.org/api/register/


Syncing data from Open States API
---------------------------------

Custom django-admin commands are used to sync data from Open States API. To pull data for
legislators and bills from Open States, run the following *in order*::

    ./djadmin.sh sync_legislators_from_openstate
    ./djadmin.sh sync_bills_from_openstate

Note that the order matters because bills have voting data which requires legislators to be
in the database for correct attribution.::

    ./djadmin.sh sync_legislators_from_openstate

The number of bills in the database is quite large. For testing purposes, you can grab a subset of
the data by using the "max" option.::

    ./djadmin.sh sync_bills_from_openstate --max 100

**Note**: openstates only provides data for the most recent session currently.


Import crosswalk CSV
--------------------

To match up the ids used by TPJ with the ids used by Openstates, we must manually create a crosswalk
then import it using the following command::

    ./djadmin.sh import_legidmap_from_csv --file [path/to/file]

**Note**: The crosswalk for the 86 session can be found inside `influencetx/legislators/data`


Basic Commands
==============

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
--------------------

The commands commonly used for maintenance of this project are described below.

- ``docker-compose -f docker-compose.dev up -d``: Start up docker container in detached mode (background task). You can
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
------------------

- ``docker-compose logs -f --tail=5``: Watch output of containers. (Alias: ``-f`` = ``--follow``.)

  - This command has a `tendency to cause timeout errors`_. If you experience timeouts, try
    running: ``COMPOSE_HTTP_TIMEOUT=60000 docker-compose logs -f``.

- ``docker-compose -f docker-compose.dev logs``: Display bash output for all containers.
- ``docker-compose -f docker-compose.dev exec web bash``: Run bash shell within web container.
- ``./djadmin.sh shell``: Start IPython shell.
- ``./djadmin.sh dbshell``: Start Postgres shell.

.. _tendency to cause timeout errors: https://github.com/docker/compose/issues/3106


Debugging Python code
---------------------

You can't use the output window from a ``docker-compose logs --f`` call to debug, since it actually
interacts with multiple containers. Instead, run the following in a terminal::

    docker attach `docker-compose -f docker-compose.dev ps -q web`

The ``docker-compose``-part of the command simply returns the id of the web container for the app.
You can replace the above with::

    docker attach influencetexas_web_1

This will attach the terminal to the web container and allow you to interact with the running
process. Now you can add a break point somewhere in your python code::

    import ipdb; ipdb.set_trace()


Settings
========

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html


Vagrant
=======

A Vagrant based deployment method is also available, which mirrors the configurations of the live
 integration/production server.
It provides a virtual machine for running the postgresql database, and is configured as a docker host.
The benefits to using an isolated VM for development is that your work is encapsulated within the VM,
 thereby allowing you to work on more than one project.
Another benefit is that by developing in an environment that is the same as the integration/production servers,
 then a CI/CD pipeline can be setup.
The primary reason for the vagrant environment was to provide a development environment for ansible development.

Pre-requisites
--------------

You must first install the following software to utilize the Vagrant development environment:

* Virtualbox_
* Ansible_
* Vagrant_

.. _VirtualBox: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwieo-Sy_YfXAhUOwGMKHR88DHsQFggvMAE&url=https%3A%2F%2Fwww.virtualbox.org%2Fwiki%2FDownloads&usg=AOvVaw2aIAdQV7iMGmQmEtwhZCT0
.. _Ansible: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwi89dTL_YfXAhUN3WMKHa25A0kQFggoMAA&url=http%3A%2F%2Fdocs.ansible.com%2Fintro_installation.html&usg=AOvVaw0QBIODybz7M47MR5vx6WwZ
.. _Vagrant: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwiptbnS_ofXAhXLq1QKHbSCDccQFggoMAA&url=https%3A%2F%2Fwww.vagrantup.com%2Fdownloads.html&usg=AOvVaw1_WWrxUNUP1qec3zvvV1Vp

Usage
-----

To start the virtual machine:

      vagrant up

To stop the virtual machine:

      vagrant halt

To open a terminal on the virtual machine:

      vagrant ssh

To rebuild and deploy the application:

      vagrant provision

Development Workflow
-------------------

There are two uses of the Vagrant environment for testing production deployments, from inside the VM or
 from outside the VM.

The Vagrant VM is run by default with the settings:
```
    vb.memory = "2048"
    vb.cpus   = "2"
```

Reduce these numbers for running on smaller hardware.

Internal
--------

To perform development from inside the VM, perform the ``vagrant ssh`` command, then change directory to "/vagrant".
  The source code is mounted automatically inside the VM at the "/vagrant" directory.
  The `docker-compose.build` file is used for deployment of the application, and allows for live updates to the source
  code.
The `pyinvoke` and `djadmin` commands do not work inside the Vagrant environment.  To perform migrations and other
 operations, use the following command::

    docker-compose -f docker-compose.build exec web python3 manage.py [command]

**Note**: Use 'help' as the command to see all available commands.


External
--------

You can also perform development outside the VM by making code updates, then issuing a `vagrant provision` command.
  This method allows SSH based checkouts of the git repository.


Production Build and Deployment
-------------------------------

This requires root privileges on the deployment server::

    ssh root@influencetx.com
    cd influence-texas
    git pull
    docker-compose build
    docker-compose up -d --force-recreate

The first `docker-compose` command builds the docker container with the influencetx codebase, and
the second starts the web application and associated services.

You can access the logs on the production server using::

    docker logs web
