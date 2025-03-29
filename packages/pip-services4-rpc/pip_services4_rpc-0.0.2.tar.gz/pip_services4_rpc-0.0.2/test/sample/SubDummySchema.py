# -*- coding: utf-8 -*-
from pip_services4_commons.convert import TypeCode
from pip_services4_data.validate import ObjectSchema


class SubDummySchema(ObjectSchema):
    def __init__(self):
        super().__init__()
        self.with_required_property('key', TypeCode.String)
        self.with_required_property('content', TypeCode.String)
