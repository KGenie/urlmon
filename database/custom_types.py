from sqlalchemy import types
import zlib


class StringList(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value, dialect):
        return ','.join(value)

    def process_result_value(self, value, dialect):
        return value.split(',')

    def copy(self):
        return StringList(self.impl.length)


class GzipBlob(types.TypeDecorator):
    impl = types.LargeBinary

    def process_bind_param(self, value, dialect):
        if value:
            return zlib.compress(value, 9)
        return value

    def process_result_value(self, value, dialect):
        if value:
            return zlib.decompress(value)
        return value

    def copy(self):
        return GzipBlob(self.impl.length)

