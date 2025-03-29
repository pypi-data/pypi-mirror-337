# -*- coding: utf-8 -*-
"""
    test.DummyService
    ~~~~~~~~~~~~~~~~~~~~
    
    Dummy Service object
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import threading
from typing import List, Optional

from pip_services4_data.keys import IdGenerator
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from pip_services4_rpc.commands import ICommandable, CommandSet
from pip_services4_components.context import IContext

from .Dummy import Dummy
from .DummyCommandSet import DummyCommandSet
from .IDummyService import IDummyService


class DummyService(IDummyService, ICommandable):

    def __init__(self):
        self.__lock = threading.Lock()
        self.__items: List[Dummy] = []
        self.__command_set: CommandSet = None

    def get_command_set(self):
        if self.__command_set is None:
            self.__command_set = DummyCommandSet(self)
        return self.__command_set

    def get_page_by_filter(self, context: Optional[IContext], filter: FilterParams, paging: PagingParams) -> DataPage:
        filters = filter if filter is not None else FilterParams()
        key = filters.get_as_nullable_string("key")

        paging = paging if not (paging is None) else PagingParams()
        skip = paging.get_skip(0)
        take = paging.get_take(100)

        result = []
        self.__lock.acquire()
        try:
            for item in self.__items:
                if not (key is None) and key != item.key:
                    continue

                skip -= 1
                if skip >= 0: continue

                take -= 1
                if take < 0: break

                result.append(item)
        finally:
            self.__lock.release()

        return DataPage(result)

    def get_one_by_id(self, context: Optional[IContext], id: str) -> Optional[Dummy]:
        self.__lock.acquire()
        try:
            for item in self.__items:
                if item.id == id:
                    return item
        finally:
            self.__lock.release()

        return None

    def create(self, context: Optional[IContext], item: Dummy) -> Dummy:
        self.__lock.acquire()
        try:
            if item.id is None:
                item.id = IdGenerator.next_long()

            self.__items.append(item)
        finally:
            self.__lock.release()

        return item

    def update(self, context: Optional[IContext], new_item: Dummy) -> Optional[Dummy]:
        self.__lock.acquire()
        try:
            for index in range(len(self.__items)):
                item = self.__items[index]
                if item.id == new_item.id:
                    self.__items[index] = new_item
                    return new_item
        finally:
            self.__lock.release()

        return None

    def delete_by_id(self, context: Optional[IContext], id: str) -> Optional[Dummy]:
        self.__lock.acquire()
        try:
            for index in range(len(self.__items)):
                item = self.__items[index]
                if item.id == id:
                    del self.__items[index]
                    return item
        finally:
            self.__lock.release()

        return None

    def check_trace_id(self, trace_id: Optional[str]) -> str:
        return trace_id
