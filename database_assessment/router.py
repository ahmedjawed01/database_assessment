class CheckerRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'bb_products':
            return 'bb_product'
        elif model._meta.app_label == 'populations':
            return 'population'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'bb_products':
            return 'bb_product'
        elif model._meta.app_label == 'populations':
            return 'population'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'bb_products' or obj2._meta.app_label == 'bb_products':
            return True
        elif 'bb_products' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        elif obj1._meta.app_label == 'populations' or obj2._meta.app_label == 'populations':
            return True
        elif 'populations' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'bb_products':
            return db == 'bb_product'
        elif app_label == 'populations':
            return db == 'population'
        return None
