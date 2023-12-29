import os
from abc import ABC, abstractmethod

from managers.manager_exceptions import ElementManagerException
from utils.utils_click import click_checkbox, click_element, focus_element
from utils.utils_get import get_input_or_textarea_elements_values
from utils.utils_set import set_first_input_field_by_send_keys_js, set_file_to_input_field, check_first_input_field, \
    find_element_and_send_keys

ELEMENT_WAIT_LIMIT_SEC = int(os.environ.get('ELEMENT_WAIT_LIMIT_SEC'))


class ElementManager(ABC):  # Parent to TextInputElementManager, CheckboxElementManager, ...
    def __init__(self, driver):
        self.driver = driver


class UpdatableElementManager(ElementManager):
    @abstractmethod
    def update(self):
        pass


class CreatableElementManager(ElementManager):
    @abstractmethod
    def create(self):
        pass


class DeletableElementManager(ElementManager):
    @abstractmethod
    def delete(self):
        pass


class CleanableElementManager(ElementManager):
    @abstractmethod
    def clean(self):
        pass


class SubmittableElementManager(ElementManager):
    @abstractmethod
    def submit(self):
        pass


class ClickableElementManager(ElementManager):
    @abstractmethod
    def click(self):
        pass


class TextInputElementManager(UpdatableElementManager):

    def __init__(self, driver, *, value_to_set: str = '', **set_input_field_kwargs):
        super().__init__(driver=driver)
        self.set_input_field_kwargs = set_input_field_kwargs
        self.value_to_set = value_to_set

    def update(self):
        set_first_input_field_by_send_keys_js(self.driver, set_value=self.value_to_set, **self.set_input_field_kwargs)

    def check_update(self):
        return check_first_input_field(self.driver, check_value=self.value_to_set, **self.set_input_field_kwargs)


class CheckboxInputElementManager(ClickableElementManager):
    def __init__(self, driver, *, set_value: bool, **element_search_kwargs):
        super().__init__(driver=driver)
        self.element_search_kwargs = element_search_kwargs
        self.set_value = set_value

    def click(self):
        click_checkbox(self.driver, set_value=self.set_value, **self.element_search_kwargs)


class ButtonElementManager(ClickableElementManager):
    def __init__(self, driver, **click_or_focus_element_kwargs):
        super().__init__(driver=driver)
        self.click_or_focus_element_kwargs = click_or_focus_element_kwargs

    def click(self):
        click_element(self.driver, **self.click_or_focus_element_kwargs)

    def focus(self):
        focus_element(self.driver, **self.click_or_focus_element_kwargs)


class SubmitElementManager(SubmittableElementManager):
    def __init__(self, driver, *, file_path, **element_search_kwargs):
        super().__init__(driver=driver)
        self.element_search_kwargs = element_search_kwargs
        self.file_path = file_path

    def submit(self):
        set_file_to_input_field(self.driver, file_path=self.file_path, **self.element_search_kwargs)


class SendKeysToElementManager(SubmittableElementManager):
    def __init__(self, driver, **send_keys_kwargs):
        super().__init__(driver=driver)
        self.send_keys_kwargs = send_keys_kwargs

    def submit(self):
        find_element_and_send_keys(self.driver, **self.send_keys_kwargs)
