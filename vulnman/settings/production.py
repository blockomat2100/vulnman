from .base import *

DEBUG = False
env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']