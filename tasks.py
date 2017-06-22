from invoke import task


@task(aliases=['dev-server'])
def dev_server(ctx, port=8512, pty=True):
    """Run django dev server."""
    ctx.run('python manage.py runserver {}'.format(port), pty=pty)
