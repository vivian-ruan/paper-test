from rest_api_framework import models
from rest_api_framework.datastore import SQLiteDataStore
from rest_api_framework.views import JsonResponse
from rest_api_framework.controllers import Controller
from rest_api_framework.datastore.validators import UniqueTogether
from rest_api_framework.pagination import Pagination

class LunModel(models.Model):

    fields = [models.StringField(name="lun_name", required=True),
              models.StringField(name="size", required=True),
              models.PkField(name="lun_id", required=True)
              ]

def remove_id(response, obj):
    obj.pop(response.model.pk_field.name)
    return obj

class UserEndPoint(Controller):
    ressource = {
        "ressource_name": "luns",
        "ressource": {"name": "lun_info.db", "table": "lun_info"},
        "model": LunModel,
        "datastore": SQLiteDataStore,
        "options": {"validators": [UniqueTogether("lun_name", "size")]}
        }

    controller = {
        "list_verbs": ["GET", "POST"],
        "unique_verbs": ["GET", "PUT", "DELETE"],
        "options": {"pagination": Pagination(5)}
        }

    view = {"response_class": JsonResponse}

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    from rest_api_framework.controllers import WSGIDispatcher
    app = WSGIDispatcher([UserEndPoint])
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
