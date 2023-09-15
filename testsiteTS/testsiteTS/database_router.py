class YourRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'crm_app':
            return 'db_from_crm'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'crm_app':
            return 'db_from_crm'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'crm_app':
            return db == 'db_from_crm'
        return db == 'default'
