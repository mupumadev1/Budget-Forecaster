class MyRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in ['Glafs','Glamf']:
            return False
        return True