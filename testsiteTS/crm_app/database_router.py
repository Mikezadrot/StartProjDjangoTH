# crm_app/database_router.py

class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'crm_app':
            return 'db_from_crm'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'crm_app':
            return 'db_from_crm'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == 'crm_app'
            or obj2._meta.app_label == 'crm_app'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'crm_app':
            return db == 'db_from_crm'
        return None
