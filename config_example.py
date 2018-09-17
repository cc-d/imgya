CONFIG_NAME='config_example'
TESTING=False
DEBUG=False
CSRF_ENABLED = True
SECRET_KEY = 'this-really-needs-to-be-changed'
SQLALCHEMY_DATABASE_URI = 'postgresql://USER:PASSWORD@IP:PORT/DATABASE'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 50 Megabytes
MAX_CONTENT_LENGTH = 50 * 1024 * 1024

UPLOAD_FOLDER = '/images/'

# ONLY SET TO TRUE IF YOU HAVE NGINX REWRITES CONFIGURED
NGINX_REWRITE = True

if NGINX_REWRITE:
        FLASK_UPLOAD_SYMLINK = '/i/'
else:
        FLASK_UPLOAD_SYMLINK = '/static/images/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'mp4', 'webm', 'ogg']
TYPE_EXTENSIONS = {'image':['png', 'jpg', 'jpeg', 'gif', 'bmp'], 'video':['mp4','webm','ogg'], 'audio':[], 'text':[]}
