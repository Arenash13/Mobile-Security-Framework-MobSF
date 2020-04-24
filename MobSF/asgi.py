import os
import django
from channels.routing import get_default_application 
from django.core.asgi import get_asgi_application
import warnings

warnings.filterwarnings('ignore', category=UserWarning, module='cffi')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MobSF.settings')
django.setup()
application = get_asgi_application()