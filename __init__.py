
import odoo.http

def always_testodoo_db_monodb(httprequest):
    return 'testodoo'

odoo.http.db_monodb = always_testodoo_db_monodb
from .import models
from . import controllers