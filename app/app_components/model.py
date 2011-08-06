
class Model(object):
    pass


class TableModelMetaclass(type):

    def __new__(cls, name, bases, attrs):

        columns = []

        form_class = attrs.get('form', None)
        if form_class:
            form = form_class()
        else:
            form = []
        exclude = attrs.get('exclude', [])
        include = attrs.get('include', [])
           
        for field in (f for f in form if f.type != 'HiddenField' and 
                f.short_name not in exclude):
            columns.append({ 'name': field.short_name, 'label':
                field.label.text })
        for name, label in include:
            columns.append({ 'name': name, 'label':label })

        if form:
            del attrs['form']
        if exclude:
            del attrs['exclude']
        if include:
            del attrs['include']
        attrs['columns'] = columns
        return super(TableModelMetaclass, cls).__new__(cls, name, bases, attrs)



class TableModel(Model):
    __metaclass__ = TableModelMetaclass

    def __init__(self, items):
        self.items = items


    def get(self, item, column_name):
        if '.' in column_name:
            split = column_name.split('.', 1)
            item = self.get(item, split[0])
            return self.get(item, split[1])
        return getattr(item, column_name, None)


    def __iter__(self):
        return iter(self.columns)
