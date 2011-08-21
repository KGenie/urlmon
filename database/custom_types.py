from sqlalchemy import types


class StringList(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value, dialect):
        return ','.join(value)

    def process_result_value(self, value, dialect):
        return value.split(',')

    def copy(self):
        return StringList(self.impl.length)
