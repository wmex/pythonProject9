from abc import ABC
from typing import List, Tuple

from managers.block_managers import ElementBlockManager, CreatableElementBlockManager, MigrationRule
from managers.manager_exceptions import ElementBlockManagerException
from utils.utils_get import get_input_or_textarea_elements_values


class PageObjectManager(ABC):

    def __init__(self, driver, unique_element_id: str):
        self.unique_element_id = unique_element_id
        self.driver = driver
        self.element_block_managers_with_rules: List[Tuple[ElementBlockManager, List[MigrationRule]]] = []

    # COMPLETED: set up flags and call migrate once
    def migrate(self) -> None:
        for (bl_mgr, migration_rules) in self.element_block_managers_with_rules:
            try:
                bl_mgr.migrate(rules=migration_rules)
            except ElementBlockManagerException:
                pass

    def refresh_active_page(self):
        self.driver.execute_script("location.reload();")

    def before_create_block_manager_event_handler(self, block_manager: ElementBlockManager):
        pass

    def after_create_block_manager_event_handler(self, block_manager: ElementBlockManager):
        self.refresh_active_page()

    def before_update_block_manager_event_handler(self, block_manager: ElementBlockManager):
        pass

    def after_update_block_manager_event_handler(self, block_manager: ElementBlockManager):
        self.refresh_active_page()

    def before_delete_block_manager_event_handler(self, block_manager: ElementBlockManager):
        pass

    def after_delete_block_manager_event_handler(self, block_manager: ElementBlockManager):
        self.refresh_active_page()

    def before_clean_block_manager_event_handler(self, block_manager: ElementBlockManager):
        pass

    def after_clean_block_manager_event_handler(self, block_manager: ElementBlockManager):
        self.refresh_active_page()
