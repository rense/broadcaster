from invoke import task


@task
def pip(context):
    context.run('pip-compile requirements.in', pty=True)
    context.run('pip-sync requirements.txt', pty=True)
