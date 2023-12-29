import logging
import os
from config import LOGGING_LEVEL
from managers.element_managers import ButtonElementManager
from managers.page_object_managers import PageObjectManager
from utils.dashboard.profile_block_managers import GrantElementBlockManager, DeadlineElementBlockManager
from managers.block_managers import MigrationRule, ElementBlockManager
from utils.utils_click import click_element, focus_element, click_checkbox
from utils.utils_set import set_first_input_field_by_send_keys_js, find_element_and_send_keys, \
    find_element_by_input_value_and_click

ELEMENT_WAIT_LIMIT_SEC = int(os.environ.get('ELEMENT_WAIT_LIMIT_SEC'))
logging.basicConfig(level=LOGGING_LEVEL)


class GrantProfilePageObjectManager(PageObjectManager):
    def __init__(self, driver, unique_element_id: str):
        super().__init__(driver, unique_element_id)
        self.element_block_managers = [
            (GrantElementBlockManager(self.driver, element_description='grant',
                                      unique_element_id=f'{self.unique_element_id}'),
             [MigrationRule.CREATE, MigrationRule.UPDATE, MigrationRule.DELETE])
        ]

    def before_block_manager_create_event_handler(self, block_manager: ElementBlockManager):
        ButtonElementManager(self.driver, text='Создать', relation_chain=['firstChild']).click()
        # super().before_block_manager_create_event_handler(block_manager)


class DeadlineProfilePageObjectManager(PageObjectManager):
    def __init__(self, driver, unique_element_id: str):
        super().__init__(driver, unique_element_id)
        self.element_block_managers = [
            (DeadlineElementBlockManager(self.driver, element_description='grant',
                                         unique_element_id=f'{self.unique_element_id}'),
             [MigrationRule.CREATE]),
            (DeadlineElementBlockManager(self.driver, element_description='grant',
                                         unique_element_id=f'{self.unique_element_id}'),
             [MigrationRule.UPDATE])
        ]

    def before_block_manager_create_event_handler(self, block_manager: ElementBlockManager):
        super().before_block_manager_create_event_handler(block_manager)
        ButtonElementManager(self.driver, text='Создать', relation_chain=['firstChild']).click()


class ProgramProfilePageObjectManager(PageObjectManager):

    def _create(self):
        click_element(self.driver, text="Программы и требования", relation_chain=['firstChild'],
                      wait_limit_sec=2, click_until_content_or_url_changes=False)
        click_element(self.driver, text='Докторантура', wait_limit_sec=10, click_until_content_or_url_changes=False)
        click_element(self.driver, text='Требования', wait_limit_sec=2, click_until_content_or_url_changes=False)
        click_element(self.driver, class_names='table-row control-row', relation_chain=['firstChild'], wait_limit_sec=2,
                      click_until_content_or_url_changes=False)
        set_first_input_field_by_send_keys_js(self.driver, inputmode='text', set_value=f'{self.unique_element_id}',
                                              wait_limit_sec=2)
        click_checkbox(self.driver, class_name='checkbox__field', set_value=True)
        click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium",
                      click_until_content_or_url_changes=True)
        # bug
        click_element(self.driver, text='Требования', wait_limit_sec=2, click_until_content_or_url_changes=False)
        click_element(self.driver, text='Факультеты и специальности', click_until_content_or_url_changes=False)
        click_element(self.driver, text='+ Добавить факультет', wait_limit_sec=2,
                      click_until_content_or_url_changes=False)
        click_element(self.driver, class_names='select__head', click_until_content_or_url_changes=False)
        click_element(self.driver, text='Логистика', class_names="select__option",
                      click_until_content_or_url_changes=False)
        click_element(self.driver, text="Сохранить", class_names="save-button btn btn--default btn--medium",
                      click_until_content_or_url_changes=False)

    def _delete(self, assert_exist=True):
        if self._find_unique_managed_element(by_page_source=True):
            click_element(self.driver, text="Программы и требования", relation_chain=['firstChild'],
                          wait_limit_sec=2, click_until_content_or_url_changes=False)
            click_element(self.driver, text='Докторантура', wait_limit_sec=2, click_until_content_or_url_changes=False)
            click_element(self.driver, text='Требования', wait_limit_sec=2, click_until_content_or_url_changes=False)
            try:
                for _ in range(5):
                    click_element(self.driver,
                                  class_names='v-icon notranslate ml-2 v-icon--link mdi mdi-delete theme--light',
                                  click_until_content_or_url_changes=False)
            except:
                click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium",
                              click_until_content_or_url_changes=False)
            click_element(self.driver, text='Требования', wait_limit_sec=2, click_until_content_or_url_changes=False)
            click_element(self.driver, text='Факультеты и специальности', click_until_content_or_url_changes=False)
            click_element(self.driver, class_names='mb-2 major-title-wrapper',
                          click_until_content_or_url_changes=False)
            click_element(self.driver,
                          class_names='v-icon notranslate v-icon--link mdi mdi-close theme--light danger--text',
                          click_until_content_or_url_changes=False)
            click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium",
                          wait_limit_sec=2, click_until_content_or_url_changes=True)
        elif assert_exist:
            raise AssertionError("Attemted to delete non-existing element with ID: %s", self.unique_element_id)


class GeneralInformationProfilePageObjectManager(PageObjectManager):
    def _create(self):
        click_element(self.driver, text='Общая информация', class_names='side-nav-link-ref',
                      wait_limit_sec=10 * 2, click_until_content_or_url_changes=False)
        set_first_input_field_by_send_keys_js(self.driver, text="Название организации",
                                              relation_chain=['firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                              set_value="Универо", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        set_first_input_field_by_send_keys_js(self.driver, text="Name of organization (eng)",
                                              relation_chain=['firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                              set_value=f"{self.unique_element_id}")
        set_first_input_field_by_send_keys_js(self.driver, text="Город",
                                              relation_chain=['firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                              set_value="Astana")
        click_element(self.driver, class_names='select__head')
        click_element(self.driver, text='Азербайджан', class_names='select__option')
        click_element(self.driver, text='+ Добавить язык', class_names='color-blue mt-2 ml-1 cursor-pointer',
                      wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        focus_element(self.driver, placeholder='Язык', wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        find_element_and_send_keys(self.driver, placeholder='Язык', keys='Keys.ENTER')
        click_element(self.driver, text='Английский', wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        set_first_input_field_by_send_keys_js(self.driver, placeholder="Описание организации",
                                              set_value="This is description",
                                              wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        set_first_input_field_by_send_keys_js(self.driver, placeholder="About organization",
                                              set_value="This is description")
        set_first_input_field_by_send_keys_js(self.driver, text='QS Ranking',
                                              relation_chain=['firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                              set_value="100-200")
        set_first_input_field_by_send_keys_js(self.driver, text='Shanghai Ranking',
                                              relation_chain=['firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                              set_value="100-200")
        click_checkbox(self.driver, label_text='Выберите то, что вы предоставляете',
                       relation_chain=['nextSibling', 'firstChild'], set_value=True)
        click_checkbox(self.driver, label_text='Выберите то, что вы предоставляете',
                       relation_chain=['nextSibling', 'nextSibling', 'firstChild'], set_value=True)
        click_checkbox(self.driver, label_text='Выберите то, что вы предоставляете',
                       relation_chain=['nextSibling', 'nextSibling', 'nextSibling', 'firstChild'], set_value=True)
        click_element(self.driver, class_names='bx.bx-x', click_until_content_or_url_changes=False)
        click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium",
                      click_until_content_or_url_changes=False)
        click_element(self.driver, text="Цены", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        click_element(self.driver, class_names="select__head", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        set_first_input_field_by_send_keys_js(self.driver, text='Бакалавриат',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'firstChild'],
                                              set_value='123')
        set_first_input_field_by_send_keys_js(self.driver, text='Бакалавриат',
                                              relation_chain=['nextSibling', 'nextSibling', 'firstChild', 'firstChild',
                                                              'firstChild', 'firstChild'], set_value='456')
        set_first_input_field_by_send_keys_js(self.driver, text='Магистратура',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'firstChild'],
                                              set_value='789')
        set_first_input_field_by_send_keys_js(self.driver, text='Магистратура',
                                              relation_chain=['nextSibling', 'nextSibling', 'firstChild', 'firstChild',
                                                              'firstChild', 'firstChild'], set_value='012')
        set_first_input_field_by_send_keys_js(self.driver, text='Докторантура',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'firstChild'],
                                              set_value='345')
        set_first_input_field_by_send_keys_js(self.driver, text='Докторантура',
                                              relation_chain=['nextSibling', 'nextSibling', 'firstChild', 'firstChild',
                                                              'firstChild', 'firstChild'], set_value='678')
        set_first_input_field_by_send_keys_js(self.driver, text='Жилье',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'firstChild'],
                                              set_value='901')
        set_first_input_field_by_send_keys_js(self.driver, text='Жилье',
                                              relation_chain=['nextSibling', 'nextSibling', 'firstChild', 'firstChild',
                                                              'firstChild', 'firstChild'], set_value='234')
        set_first_input_field_by_send_keys_js(self.driver, text='Питание',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'firstChild'],
                                              class_names='col col-12', set_value='154')
        click_element(self.driver, text='Доллар', class_names='select__option',
                      wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
        click_element(self.driver, text="Условия обучения", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        set_first_input_field_by_send_keys_js(self.driver, text='В стоимость обучения входит (рус)',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'nextSibling', 'firstChild'],
                                              set_value="Description of cost")
        set_first_input_field_by_send_keys_js(self.driver, text='Дополнительные платные услуги (рус)',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'nextSibling', 'firstChild'],
                                              set_value="Additional paid service")
        set_first_input_field_by_send_keys_js(self.driver, text='Дополнительные платные услуги (англ.)',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'nextSibling', 'firstChild'],
                                              set_value="Additional paid service")
        click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
        click_element(self.driver, text="Медиа", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        set_first_input_field_by_send_keys_js(self.driver, inputmode="text", set_value="C3GouGa0noM",
                                              wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC)
        click_element(self.driver, class_names='select__head')
        click_element(self.driver, class_names='select__option')
        click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
        click_element(self.driver, text="Ссылки", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        set_first_input_field_by_send_keys_js(self.driver, id="youtube_link", set_value="www.youtube.com")
        set_first_input_field_by_send_keys_js(self.driver, id="insta_link", set_value="www.instagram.kz")
        set_first_input_field_by_send_keys_js(self.driver, id="vk_link", set_value="www.vk.ru")
        set_first_input_field_by_send_keys_js(self.driver, id="telegram_link", set_value="www.telegram.ae")
        set_first_input_field_by_send_keys_js(self.driver, id="twitter_link", set_value="www.twitter.cum")
        set_first_input_field_by_send_keys_js(self.driver, id="facebook_link", set_value="www.facebook.com")
        set_first_input_field_by_send_keys_js(self.driver, id="linkedin_link", set_value="www.linkedin.com")
        click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
        click_element(self.driver, text="Программы обмена", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        set_first_input_field_by_send_keys_js(self.driver,
                                              text='Опишите доступные программы студенческого обмена (рус)',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'nextSibling', 'firstChild'],
                                              set_value="This is student transfer")
        set_first_input_field_by_send_keys_js(self.driver,
                                              text='Опишите доступные программы студенческого обмена (англ.)',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'nextSibling', 'firstChild'],
                                              set_value="This is student transfer(english)")
        click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
        click_element(self.driver, text="Достижения", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
        set_first_input_field_by_send_keys_js(self.driver,
                                              text='Перечислите награды и достижения вашей организации (рус)',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'nextSibling', 'firstChild'], set_value="Achievements")
        set_first_input_field_by_send_keys_js(self.driver,
                                              text='Перечислите награды и достижения вашей организации (англ.)',
                                              relation_chain=['nextSibling', 'firstChild', 'firstChild', 'firstChild',
                                                              'nextSibling', 'firstChild'], set_value="4755mmr")
        click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
        click_element(self.driver, text='Общая информация', class_names='side-nav-link-ref',
                      wait_limit_sec=10 * 2)

    def _delete(self, assert_exists=True):
        if self._find_unique_managed_element(by_element_value=True):
            click_element(self.driver, text='Общая информация', class_names='side-nav-link-ref',
                          wait_limit_sec=10 * 2, click_until_content_or_url_changes=False)
            set_first_input_field_by_send_keys_js(self.driver, text="Название организации",
                                                  relation_chain=['firstChild', 'firstChild', 'firstChild',
                                                                  'firstChild'],
                                                  set_value="", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
            set_first_input_field_by_send_keys_js(self.driver, text="Name of organization (eng)",
                                                  relation_chain=['firstChild', 'firstChild', 'firstChild',
                                                                  'firstChild'],
                                                  set_value=f"{self.unique_element_id}")
            set_first_input_field_by_send_keys_js(self.driver, text="Город",
                                                  relation_chain=['firstChild', 'firstChild', 'firstChild',
                                                                  'firstChild'],
                                                  set_value="")
            set_first_input_field_by_send_keys_js(self.driver, placeholder="Описание организации", set_value="",
                                                  wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
            set_first_input_field_by_send_keys_js(self.driver, placeholder="About organization", set_value="")
            set_first_input_field_by_send_keys_js(self.driver, text='QS Ranking',
                                                  relation_chain=['firstChild', 'firstChild', 'firstChild',
                                                                  'firstChild'],
                                                  set_value="")
            set_first_input_field_by_send_keys_js(self.driver, text='Shanghai Ranking',
                                                  relation_chain=['firstChild', 'firstChild', 'firstChild',
                                                                  'firstChild'],
                                                  set_value="")
            click_checkbox(self.driver, label_text='Гранты', relation_chain=['firstChild'], set_value=False)
            click_checkbox(self.driver, label_text='Двойные специальносьти', relation_chain=['firstChild'],
                           set_value=False)
            click_checkbox(self.driver, label_text='Двойной диплом', relation_chain=['firstChild'], set_value=False)
            click_element(self.driver, class_names='bx.bx-x')
            click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
            click_element(self.driver, text="Цены", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
            click_element(self.driver, class_names="select__head", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
            set_first_input_field_by_send_keys_js(self.driver, text='Бакалавриат',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'firstChild'],
                                                  set_value='')
            set_first_input_field_by_send_keys_js(self.driver, text='Бакалавриат',
                                                  relation_chain=['nextSibling', 'nextSibling', 'firstChild',
                                                                  'firstChild',
                                                                  'firstChild', 'firstChild'], set_value='')
            set_first_input_field_by_send_keys_js(self.driver, text='Магистратура',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'firstChild'],
                                                  set_value='')
            set_first_input_field_by_send_keys_js(self.driver, text='Магистратура',
                                                  relation_chain=['nextSibling', 'nextSibling', 'firstChild',
                                                                  'firstChild',
                                                                  'firstChild', 'firstChild'], set_value='')
            set_first_input_field_by_send_keys_js(self.driver, text='Докторантура',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'firstChild'],
                                                  set_value='')
            set_first_input_field_by_send_keys_js(self.driver, text='Докторантура',
                                                  relation_chain=['nextSibling', 'nextSibling', 'firstChild',
                                                                  'firstChild',
                                                                  'firstChild', 'firstChild'], set_value='')
            set_first_input_field_by_send_keys_js(self.driver, text='Жилье',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'firstChild'],
                                                  set_value='')
            set_first_input_field_by_send_keys_js(self.driver, text='Жилье',
                                                  relation_chain=['nextSibling', 'nextSibling', 'firstChild',
                                                                  'firstChild',
                                                                  'firstChild', 'firstChild'], set_value='')
            set_first_input_field_by_send_keys_js(self.driver, text='Питание',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'firstChild'],
                                                  class_names='col col-12', set_value='')
            click_element(self.driver, text='Доллар', class_names='select__option',
                          wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
            click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
            click_element(self.driver, text="Условия обучения", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
            set_first_input_field_by_send_keys_js(self.driver, text='В стоимость обучения входит (рус)',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'nextSibling', 'firstChild'], set_value="")
            set_first_input_field_by_send_keys_js(self.driver, text='Дополнительные платные услуги (рус)',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'nextSibling', 'firstChild'], set_value="")
            set_first_input_field_by_send_keys_js(self.driver, text='Дополнительные платные услуги (англ.)',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'nextSibling', 'firstChild'], set_value="")
            click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
            click_element(self.driver, text="Медиа", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
            set_first_input_field_by_send_keys_js(self.driver, inputmode="text", set_value="",
                                                  wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC)
            click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
            click_element(self.driver, text="Ссылки", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
            set_first_input_field_by_send_keys_js(self.driver, id="youtube_link", set_value="")
            set_first_input_field_by_send_keys_js(self.driver, id="insta_link", set_value="")
            set_first_input_field_by_send_keys_js(self.driver, id="vk_link", set_value="")
            set_first_input_field_by_send_keys_js(self.driver, id="telegram_link", set_value="")
            set_first_input_field_by_send_keys_js(self.driver, id="twitter_link", set_value="")
            set_first_input_field_by_send_keys_js(self.driver, id="facebook_link", set_value="")
            set_first_input_field_by_send_keys_js(self.driver, id="linkedin_link", set_value="")
            click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
            click_element(self.driver, text="Программы обмена", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
            set_first_input_field_by_send_keys_js(self.driver,
                                                  text='Опишите доступные программы студенческого обмена (рус)',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'nextSibling', 'firstChild'], set_value="")
            set_first_input_field_by_send_keys_js(self.driver,
                                                  text='Опишите доступные программы студенческого обмена (англ.)',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'nextSibling', 'firstChild'], set_value="")
            click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")
            click_element(self.driver, text="Достижения", wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC * 2)
            set_first_input_field_by_send_keys_js(self.driver,
                                                  text='Перечислите награды и достижения вашей организации (рус)',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'nextSibling', 'firstChild'], set_value="")
            set_first_input_field_by_send_keys_js(self.driver,
                                                  text='Перечислите награды и достижения вашей организации (англ.)',
                                                  relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                  'firstChild',
                                                                  'nextSibling', 'firstChild'], set_value="")
            click_element(self.driver, text="Сохранить", class_names="btn btn--default btn--medium")

        elif assert_exists:
            raise AssertionError("Attemted to delete non-existing element with ID: %s", self.unique_element_id)
