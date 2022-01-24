import sys, os, django
sys.path.append("/path/to/market")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "market.settings")
django.setup()

from portfolio.models import *

CurrentPortfolio.objects.create(username = 'test1', current = "PERSONAL")
