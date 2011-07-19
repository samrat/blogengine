import os

SECRET_KEY = 'abcdefg'
DEBUG = True

SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(os.path.dirname(__file__),'blogengine.db'))

#'sqlite:///%s/blogengine.db' % os.path.dirname(__file__)

#print SQLALCHEMY_DATABASE_URI
#print os.path.dirname(__file__)
