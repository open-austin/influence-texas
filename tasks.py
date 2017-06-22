from invoke import task


@task(aliases=['dev-server'])
def dev_server(ctx, port=8512, pty=True):
    """Run django dev server."""
    ctx.run('python manage.py runserver {}'.format(port), pty=pty)


@task(aliases=['create-app'])
def create_app(ctx, app_name, pty=True):
    """Create Django new 'app'.

    In addition to running the django `startapp` manage command, this also adds the appropriate
    app directory.
    """
    app_dir = f'./influencetx/{app_name}/'
    ctx.run(f'mkdir {app_dir}', pty=pty)
    # For some reason, ``python manage.py ...` throws a name error, but `django-admin.py` doesn't.
    ctx.run(f'django-admin.py startapp {app_name} {app_dir}', pty=pty)

    url = f"url(r'^{app_name}/', include('influencetx.{app_name}.urls', namespace='{app_name}')),"
    print("\nYou may also want to add the following url pattern to `config/urls.py`:\n")
    print(f"   {url}")
    print("\nAnd the following item to the `INSTALLED_APPS` list in `config/settings/base.py`:\n")
    print(f"   'influencetx.{app_name}',\n")
