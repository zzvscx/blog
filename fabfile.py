from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "blog"

env.user = 'ubuntu'
env.password = 'zxcasd123'
env.hosts = ['111.231.87.162']
env.port = '22'

def deploy():
    source_folder = '/home/ubuntu/sites/demo.zz.com/blog'
    run('cd {} && git pull '.format(source_folder))
    run(
        '''
        cd {} &&
        ../venv_blog/bin/pip install -r requirements.txt &&
        ../venv_blog/bin/python manage.py collectstatic --noinput &&
        ../venv_blog/bin/python manage.py migrate
        '''.format(source_folder))
    sudo('restart gunicorn-demo.zz.com')
    sudo('service nginx reload')