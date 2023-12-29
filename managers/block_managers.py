import dataclasses
from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from managers.manager_exceptions import ElementBlockManagerException, ElementBlockManagerException, ElementBlockManagerException, \
    ElementBlockManagerException, ElementBlockManagerException
from utils.utils_get import count_elements


# @dataclasses.dataclass
# class MigrationRules:
#     create: bool = False
#     refresh_page_after_create: bool = False
#     check_create: bool = False
#     update: bool = False
#     check_update: bool = False
#     delete: bool = False
#     check_delete: bool = False
#     clean: bool = False
#     check_clean: bool = False


class MigrationRule(Enum):
    CREATE = 0
    CHECK_CREATE = 1
    UPDATE = 2
    CHECK_UPDATE = 3
    DELETE = 4
    CHECK_DELETE = 5
    CLEAN = 6
    CHECK_CLEAN = 7

# COMPLETED: log exceptions just before raising them
# COMPLETED: Simplify exceptions where possible (ElementBlockManagerException is probably enough for all test cases)


class ElementBlockManager(ABC):  # parent to GrantElementBlockManager, ...
    def __init__(self, driver, unique_element_id: str, **kwargs):
        self.driver = driver
        self.unique_element_id = unique_element_id
        self.logger_manager = UniveroLoggerManager(self.driver)

    def migrate(self, rules: List[MigrationRule]) -> None:
        for rule in rules:
            if rule == MigrationRule.CLEAN:
                try:
                    self._clean()
                except ElementBlockManagerException as e:
                    self.logger_manager.log_exception(e)
                    self.logger_manager.append_in_html()
            elif rule == MigrationRule.CHECK_CLEAN:
                try:
                    self._check_clean()
                except ElementBlockManagerException as e:
                    self.logger_manager.log_exception(e)
                    self.logger_manager.append_in_html()
            elif rule == MigrationRule.UPDATE:
                try:
                    self._update()
                except ElementBlockManagerException as e:
                    self.logger_manager.log_exception(e)
                    self.logger_manager.append_in_html()
            elif rule == MigrationRule.CHECK_UPDATE:
                try:
                    self._check_update()
                except ElementBlockManagerException as e:
                    self.logger_manager.log_exception(e)
                    self.logger_manager.append_in_html()
            elif rule == MigrationRule.DELETE:
                try:
                    self._delete()
                except ElementBlockManagerException as e:
                    self.logger_manager.log_exception(e)
                    self.logger_manager.append_in_html()
            elif rule == MigrationRule.CHECK_DELETE:
                try:
                    self._check_delete()
                except ElementBlockManagerException as e:
                    self.logger_manager.log_exception(e)
                    self.logger_manager.append_in_html()

    @abstractmethod
    def _update(self) -> None:
        pass

    @abstractmethod
    def _check_update(self) -> None:
        pass

    @abstractmethod
    def _delete(self) -> None:
        pass

    @abstractmethod
    def _check_delete(self) -> None:
        pass

    @abstractmethod
    def _clean(self) -> None:
        pass

    @abstractmethod
    def _check_clean(self) -> None:
        pass
# COMPLETED: remove "rules" argument from all methods except migrate


class CreatableElementBlockManager(ElementBlockManager):
    def __init__(self, driver, unique_element_id: str, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)

    def migrate(self, rules: List[MigrationRule]) -> None:
        for rule in rules:
            if rule not in (MigrationRule.CREATE, MigrationRule.CHECK_CREATE):
                super().migrate(rules=[rule])
            elif rule == MigrationRule.CREATE:
                try:
                    self._create()
                except ElementBlockManagerException as e:
                    self.logger_manager.log_exception(e)
                    self.logger_manager.append_in_html()
                    raise ElementBlockManagerException(e)
            elif rule == MigrationRule.CHECK_CREATE:
                try:
                    self._check_create()
                except ElementBlockManagerException as e:
                    self.logger_manager.log_exception(e)
                    self.logger_manager.append_in_html()
                    raise ElementBlockManagerException(e)

    @abstractmethod
    def _create(self) -> None:
        pass

    @abstractmethod
    def _check_create(self) -> None:
        pass

class BlockCounter:
    def __init__(self, driver, attribute_name, attribute_value):
        self.driver = driver
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value

    def count_blocks(self):
        result = count_elements(
            self.driver, attribute_name=f'{self.attribute_name}',
            attribute_value=f'{self.attribute_value}')
        return result

# BlockBatcher
