from django.conf import settings


TPJ_APP = 'tpj'


class DatabaseRouter(object):
    """Database router that routes to TPJ db for `tpj` app and associated models."""

    def db_for_read(self, model, **hints):
        return get_database_config_for_model_or_default(model)

    def db_for_write(self, model, **hints):
        return get_database_config_for_model_or_default(model)

    def allow_relation(self, obj1, obj2, **hints):
        # Only allow relations for models in the same database.
        app1 = getattr(obj1._meta, 'app_label', None)
        app2 = getattr(obj2._meta, 'app_label', None)
        # Always allow relations in the same app, never allow relations to cross TPJ app boundary.
        return app1 == app2 or not (app1 == TPJ_APP or app2 == TPJ_APP)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return not (app_label == TPJ_APP or db == 'tpj')


def get_database_config_for_model_or_default(model):
    db = getattr(model._meta, 'app_label', None)
    return db if db in settings.DATABASES else None
