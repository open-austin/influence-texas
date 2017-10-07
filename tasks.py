import os
from warnings import warn

from invoke import task


@task()
def test(ctx, path='influencetx', coverage=True, capture=False, pty=True):
    """Run test suite.

    To limit the tests that are run, pass a `--path` argument to the test command:

        test --path influencetx/candidates
    """
    test_cmd = 'pytest'
    test_cmd += ' --cov=influencetx --cov-report term-missing' if coverage else ''
    test_cmd += '' if capture else ' --capture=no'
    ctx.run(f'{test_cmd} {path}', pty=pty)


@task()
def install(ctx, packages, pty=True):
    """Install packages using pip."""
    package_args = csv_to_args(packages)
    ctx.run(f'pip install {package_args}', pty=pty)


@task(aliases=['install-requirements'])
def install_requirements(ctx, pty=True):
    """Install local requirements using pip.

    Local requirements are installed when starting up the docker container, but you'll need to run
    this command if you pull code from github that includes updates to requirements files.
    """
    ctx.run(f'pip install -r requirements/local.txt', pty=pty)


@task()
def check(ctx, pty=True):
    """Check project for any problems."""
    ctx.run(f'python manage.py check', pty=pty)
    ctx.run(f'flake8', pty=pty)


@task(aliases=['create-app'])
def create_app(ctx, app_name, pty=True):
    """Create new Django 'app'.

    In addition to running the django `startapp` manage command, this also adds the appropriate
    app directory.
    """
    app_dir = f'./influencetx/{app_name}/'
    ctx.run(f'mkdir {app_dir}', pty=pty)
    # For some reason, ``python manage.py ...` throws a name error, but `django-admin.py` doesn't.
    ctx.run(f'django-admin.py startapp {app_name} {app_dir}', pty=pty)

    url = f"url(r'^{app_name}/', include('influencetx.{app_name}.urls', namespace='{app_name}')),"
    apps_module_path = f'influencetx/{app_name}/apps.py'
    url_module_path = f'influencetx/{app_name}/urls.py'
    full_app_path = f'influencetx.{app_name}'
    template_path = f'influencetx/templates/{app_name}'
    view_docs = 'https://docs.djangoproject.com/en/1.11/intro/tutorial03/'

    print(f"\nCreated {app_dir!r}.\n")
    print("\nYou may also want to do the following:")
    print(f"- Change `name = '{app_name}'` to `name = '{full_app_path}'` in '{apps_module_path}'")
    print(f"- Add app to `LOCAL_APPS` list in `config/settings/base.py`: '{full_app_path}',")
    print(f"- Add view for your new app: {view_docs}")
    print(f"- Add url pattern to `config/urls.py`: {url}")
    print(f"- Add template subdirectory for new app: mkdir {template_path}")


def csv_to_args(csv_string):
    return ' '.join(csv_string.split(','))
