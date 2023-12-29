from managers.block_managers import CreatableElementBlockManager, BlockCounter, ElementBlockManager
from managers.element_managers import TextInputElementManager, ButtonElementManager, SendKeysToElementManager, \
    SubmitElementManager
from managers.manager_exceptions import ElementBlockManagerException, ElementBlockManagerException, ElementBlockManagerException
from utils.utils_set import find_element_by_input_value_and_click, find_element_and_send_keys


# COMPLETED:
#  1. Contain block element manager's element search to its outermost container element
#     https://chat.openai.com/share/489f72be-3eba-4600-9f49-30cfb4beb0ad
#  2. For each MigrationRule create one or two abstract event handlers (taking element block manager as an argument )
#     in the base page object manager, and call them from element block managers at the appropriate moments.
#  3. Saving or refreshing the page should only be done in the page object manager (e.g. in the event handlers).
#  4. Migrations should be controlled by the list of migration rules passed into the element block manager's migrate method.
#  5. The page object manager you test your code on should be the most complex one (or several) to test all edge cases.
#  6. It is not always possible to hardcode the block element manager(s) you work with, so they must be identified
#     dynamically (e.g. by their xpath) and their identifying selector should be passed to the created
#     block element manager's  constructor at its creation.


class GrantElementBlockManager(CreatableElementBlockManager):
    def __init__(self, driver, unique_element_id, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)

        self.elements = [
            TextInputElementManager(self.driver, container_xpath='/html/body/div/div/div/div/div[2]/div/div/div/div[1]',
                                    inputmodee='text',
                                    value_to_set=self.unique_element_id),
            TextInputElementManager(self.driver, container_xpath='/html/body/div/div/div/div/div[2]/div/div/div/div[1]',
                                    placeholder='Добавьте информацию о гранте (что покрывает, требования для абитуриента, ...)',
                                    value_to_set='This is grant description')
        ]
        self.block_counter = BlockCounter(self.driver, attribute_name='placeholder',
                                          attribute_value='Добавьте информацию о гранте (что покрывает, требования для абитуриента, ...)')

        self.goto_grant_page = ButtonElementManager(self.driver, text="Гранты, стипендии, скидки",
                                                    relation_chain=['firstChild'],
                                                    click_until_content_or_url_changes=False)
        self.create_block_button = ButtonElementManager(self.driver, text="+ Добавить блок",
                                                        relation_chain=['firstChild'],
                                                        click_until_content_or_url_changes=False)

        self.goto_grant_page.click()
        self.init_block_count = self.block_counter.count_blocks()
        self.save_grant_block_button = ButtonElementManager(self.driver, text="Создать",
                                                            click_until_content_or_url_changes=False)

    def _create(self) -> None:
        self.create_block_button.click()

    def _check_create(self) -> None:
        if not self.block_counter.count_blocks() == self.init_block_count + 1:
            raise ElementBlockManagerException('Failed to create grant block')

    def _update(self) -> None:
        for el in self.elements:
            el.update()

    def _check_update(self) -> None:
        # CHECK UPDATE
        for el in self.elements:
            if not el.check_update:
                raise ElementBlockManagerException("Failed to update grant block")
        self.save_grant_block_button.click()

    def _delete(self) -> None:
        find_element_by_input_value_and_click(self.driver, value=self.unique_element_id,
                                              relation_chain=['Parent', 'Parent', 'Parent', 'Parent', 'Parent',
                                                              'nextSibling', 'nextSibling', 'lastChild'])

    def _check_delete(self) -> None:
        # CHECK DELETE
        if not self.block_counter.count_blocks() == self.init_block_count:
            raise ElementBlockManagerException('Failed to delete grant block')

    def _clean(self) -> None:
        pass

    def _check_clean(self) -> None:
        pass


class DeadlineElementBlockManager(CreatableElementBlockManager):
    def __init__(self, driver, unique_element_id, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)
        self.elements = [
            TextInputElementManager(self.driver, text='Создать',
                                    relation_chain=['prevSibling', 'prevSibling', 'prevSibling', 'firstChild',
                                                    'firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                    value_to_set=self.unique_element_id),
            TextInputElementManager(self.driver, text='Создать',
                                    relation_chain=['prevSibling', 'prevSibling', 'prevSibling', 'lastChild',
                                                    'firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                    value_to_set='https://stage.univero.cc/'),
            TextInputElementManager(self.driver, text='Создать',
                                    relation_chain=['prevSibling', 'firstChild', 'lastChild', 'firstChild',
                                                    'firstChild', 'firstChild'], inputmode_content='date',
                                    value_to_set='1111-11-11'),
            TextInputElementManager(self.driver, text='Создать',
                                    relation_chain=['prevSibling', 'lastChild', 'lastChild', 'firstChild',
                                                    'firstChild', 'firstChild'], inputmode_content='date',
                                    value_to_set='1111-11-12')]
        self.block_counter = BlockCounter(self.driver, attribute_name='class', attribute_value='v-card__title')
        self.goto_deadline_page = ButtonElementManager(self.driver, text="Дедлайны", relation_chain=['firstChild'],
                                                       wait_limit_sec=10, click_until_content_or_url_changes=False)
        self.goto_deadline_page.click()
        self.create_deadline_block = ButtonElementManager(self.driver, text="Добавить +",
                                                          class_names='btn btn--success btn--medium',
                                                          wait_limit_sec=2)
        self.select_program = ButtonElementManager(self.driver, text="Создать",
                                                   relation_chain=['prevSibling', 'prevSibling', 'firstChild',
                                                                   'firstChild', 'firstChild'])
        self.select_program_option = ButtonElementManager(self.driver, text="Создать",
                                                          relation_chain=['prevSibling', 'prevSibling', 'firstChild',
                                                                          'firstChild', 'lastChild', 'firstChild',
                                                                          'firstChild', 'firstChild'])
        self.save_deadline_block = ButtonElementManager(self.driver, text="Создать", relation_chain=['firstChild'])
        self.delete_deadline_block = ButtonElementManager(self.driver,
                                                          container_xpath='/html/body/div/div/div/div/div[2]/div/div/div/div[3]',
                                                          text='Удалить дедлайн')

    def _create(self) -> None:
        self.init_block_count = self.block_counter.count_blocks()
        self.create_deadline_block.click()

    def _check_create(self) -> None:
        if not self.block_counter.count_blocks() == self.init_block_count + 1:
            raise ElementBlockManagerException('Failed to create deadline block')

    def _update(self) -> None:
        for el in self.elements:
            el.update()

    def _check_update(self) -> None:
        for el in self.elements:
            if not el.check_update():
                raise ElementBlockManagerException(f'Failed to update deadline element: {el}')
        self.save_deadline_block.click()

    def _delete(self) -> None:
        self.delete_deadline_block.click()

    def _check_delete(self) -> None:
        if not self.block_counter.count_blocks() == self.init_block_count:
            raise ElementBlockManagerException('Failed to delete deadline block')

    def _clean(self) -> None:
        pass

    def _check_clean(self) -> None:
        pass


class AboutGeneralInformationInputBlockElementManager(ElementBlockManager):
    def __init__(self, driver, unique_element_id, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)
        self.elements = [
            TextInputElementManager(self.driver, text="Название организации",
                                    relation_chain=['firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                    set_value="Универо", wait_limit_sec=10),
            TextInputElementManager(self.driver, text="Name of organization (eng)",
                                    relation_chain=['firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                    set_value=f"{self.unique_element_id}"),
            TextInputElementManager(self.driver, text="Город",
                                    relation_chain=['firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                    set_value="Astana"),
            TextInputElementManager(self.driver, placeholder="Описание организации", set_value="This is description",
                                    wait_limit_sec=10),
            TextInputElementManager(self.driver, placeholder="About organization", set_value="This is description"),
            TextInputElementManager(self.driver, text='QS Ranking',
                                    relation_chain=['firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                    set_value="100-200"),
            TextInputElementManager(self.driver, text='Shanghai Ranking',
                                    relation_chain=['firstChild', 'firstChild', 'firstChild', 'firstChild'],
                                    set_value="100-200")]
        self.save_button = ButtonElementManager(self.driver, text="Сохранить",
                                                class_names="btn btn--default btn--medium")

    def _update(self) -> None:
        for el in self.elements:
            el.update()

    def _check_update(self) -> None:
        for el in self.elements:
            if not el.check_update():
                raise ElementBlockManagerException(
                    f'Failed to update input element in About General Information Page: {el}')

    def _delete(self) -> None:
        pass

    def _check_delete(self) -> None:
        pass

    def _clean(self) -> None:
        for el in self.elements:
            el.value_to_set = ''
            el.update()

    def _check_clean(self) -> None:
        for el in self.elements:
            el.value_to_set = ''
            if not el.check_update():
                raise ElementBlockManagerException(
                    f'Failed to clean input element in About General Information Page: {el}')


class AboutGeneralInformationLanguageBlockElementManager(CreatableElementBlockManager):
    def __init__(self, driver, unique_element_id: str, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)
        self.create_language_block = ButtonElementManager(self.driver, text='+ Добавить язык',
                                                          class_names='color-blue mt-2 ml-1 cursor-pointer',
                                                          wait_limit_sec=3)
        self.select_language_option = ButtonElementManager(self.driver, placeholder='Язык', wait_limit_sec=3)
        self.select_language = SendKeysToElementManager(self.driver, placeholder='Язык', keys='Keys.ENTER')
        self.delete_language_block = ButtonElementManager(self.driver, class_names='btn-remove')

    def _create(self) -> None:
        self.create_language_block.click()

    def _check_create(self) -> None:
        pass

    def _update(self) -> None:
        self.select_language_option.focus()
        self.select_language.submit()

    def _check_update(self) -> None:
        pass

    def _delete(self) -> None:
        self.delete_language_block.click()

    def _check_delete(self) -> None:
        pass

    def _clean(self) -> None:
        pass

    def _check_clean(self) -> None:
        pass


class AboutGeneralInformationSubmitBlockElementManager(ElementBlockManager):
    def __init__(self, driver, unique_element_id: str, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)
        self.submit_file = SubmitElementManager(self.driver, file_path='resourses/image.png', id='fileItem')
        self.delete_file = ButtonElementManager(self.driver, class_names='bx bx-x')

    def _update(self) -> None:
        self.submit_file.submit()

    def _check_update(self) -> None:
        pass

    def _delete(self) -> None:
        self.delete_file.click()

    def _check_delete(self) -> None:
        pass

    def _clean(self) -> None:
        pass

    def _check_clean(self) -> None:
        pass


class PricesGeneralInformationBlockElementManager(ElementBlockManager):
    def __init__(self, driver, unique_element_id, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)
        self.elements = [TextInputElementManager(self.driver, text='Бакалавриат',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild',
                                                                 'firstChild'], set_value='123'),
                         TextInputElementManager(self.driver, text='Бакалавриат',
                                                 relation_chain=['nextSibling', 'nextSibling', 'firstChild',
                                                                 'firstChild', 'firstChild', 'firstChild'],
                                                 set_value='456'),
                         TextInputElementManager(self.driver, text='Магистратура',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild', 'firstChild'], set_value='789'),
                         TextInputElementManager(self.driver, text='Магистратура',
                                                 relation_chain=['nextSibling', 'nextSibling', 'firstChild',
                                                                 'firstChild', 'firstChild', 'firstChild'],
                                                 set_value='012'),
                         TextInputElementManager(self.driver, text='Докторантура',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild', 'firstChild'],
                                                 set_value='345'),
                         TextInputElementManager(self.driver, text='Докторантура',
                                                 relation_chain=['nextSibling', 'nextSibling', 'firstChild',
                                                                 'firstChild', 'firstChild', 'firstChild'],
                                                 set_value='678'),
                         TextInputElementManager(self.driver, text='Жилье',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild', 'firstChild'], set_value='901'),
                         TextInputElementManager(self.driver, text='Жилье',
                                                 relation_chain=['nextSibling', 'nextSibling', 'firstChild',
                                                                 'firstChild',
                                                                 'firstChild', 'firstChild'], set_value='234'),
                         TextInputElementManager(self.driver, text='Питание',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild', 'firstChild'],
                                                 class_names='col col-12', set_value='154')]
        self.select_currency_option = ButtonElementManager(self.driver, class_names="select__head", wait_limit_sec=3)
        self.select_currency = ButtonElementManager(self.driver, text='Доллар', class_names='select__option',
                                                    wait_limit_sec=3)
        self.goto_prices_page = ButtonElementManager(self.driver, text="Цены", wait_limit_sec=3)

    def _update(self) -> None:
        pass

    def _check_update(self) -> None:
        pass

    def _clean(self) -> None:
        pass

    def _check_clean(self) -> None:
        pass

    def _delete(self) -> None:
        pass

    def _check_delete(self) -> None:
        pass


class ConditionsGeneralInformationBlockElementManager(ElementBlockManager):
    def __init__(self, driver, unique_element_id, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)
        self.elements = [TextInputElementManager(self.driver, text='В стоимость обучения входит (рус)',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild', 'nextSibling', 'firstChild'],
                                                 set_value="Description of cost"),
                         TextInputElementManager(self.driver, text='Дополнительные платные услуги (рус)',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild', 'nextSibling', 'firstChild'],
                                                 set_value="Additional paid service"),
                         TextInputElementManager(self.driver, text='Дополнительные платные услуги (англ.)',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild', 'nextSibling', 'firstChild'],
                                                 set_value="Additional paid service")]
        self.goto_conditions_page = ButtonElementManager(self.driver, text="Условия обучения", wait_limit_sec=3)

    def _update(self) -> None:
        pass

    def _check_update(self) -> None:
        pass

    def _clean(self) -> None:
        pass

    def _check_clean(self) -> None:
        pass

    def _delete(self) -> None:
        pass

    def _check_delete(self) -> None:
        pass


class MediaGeneralInformationBlockElementManager(ElementBlockManager):
    def __init__(self, driver, unique_element_id, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)
        self.elements = [TextInputElementManager(self.driver, inputmode="text", set_value="C3GouGa0noM",
                                                 wait_limit_sec=3)]
        self.goto_media_page = ButtonElementManager(self.driver, text="Медиа", wait_limit_sec=3)
        self.select_image_option = ButtonElementManager(self.driver, class_names='select__head')
        self.select_image = ButtonElementManager(self.driver, class_names='select__option')

    def _update(self) -> None:
        pass

    def _check_update(self) -> None:
        pass

    def _clean(self) -> None:
        pass

    def _check_clean(self) -> None:
        pass

    def _delete(self) -> None:
        pass

    def _check_delete(self) -> None:
        pass


class LinksGeneralInformationBlockElementManager(ElementBlockManager):
    def __init__(self, driver, unique_element_id, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)
        self.elements = [TextInputElementManager(self.driver, id="youtube_link", set_value="www.youtube.com"),
                         TextInputElementManager(self.driver, id="insta_link", set_value="www.instagram.kz"),
                         TextInputElementManager(self.driver, id="vk_link", set_value="www.vk.ru"),
                         TextInputElementManager(self.driver, id="telegram_link", set_value="www.telegram.ae"),
                         TextInputElementManager(self.driver, id="twitter_link", set_value="www.twitter.cum"),
                         TextInputElementManager(self.driver, id="facebook_link", set_value="www.facebook.com"),
                         TextInputElementManager(self.driver, id="linkedin_link", set_value="www.linkedin.com")]
        self.goto_links_page = ButtonElementManager(self.driver, text="Ссылки", wait_limit_sec=3)

    def _update(self) -> None:
        pass

    def _check_update(self) -> None:
        pass

    def _clean(self) -> None:
        pass

    def _check_clean(self) -> None:
        pass

    def _delete(self) -> None:
        pass

    def _check_delete(self) -> None:
        pass


class ExchangeProgramsGeneralInformationBlockElementManager(ElementBlockManager):
    def __init__(self, driver, unique_element_id, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)
        self.elements = [TextInputElementManager(self.driver,
                                                 text='Опишите доступные программы студенческого обмена (рус)',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild',
                                                                 'nextSibling', 'firstChild'],
                                                 set_value="This is student transfer"),
                         TextInputElementManager(self.driver,
                                                 text='Опишите доступные программы студенческого обмена (англ.)',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild',
                                                                 'nextSibling', 'firstChild'],
                                                 set_value="This is student transfer(english)")]
        self.goto_exchange_program_page = ButtonElementManager(self.driver, text="Программы обмена", wait_limit_sec=3)

    def _update(self) -> None:
        pass

    def _check_update(self) -> None:
        pass

    def _clean(self) -> None:
        pass

    def _check_clean(self) -> None:
        pass

    def _delete(self) -> None:
        pass

    def _check_delete(self) -> None:
        pass


class AchievmentsGeneralInformationBlockElementManager(ElementBlockManager):
    def __init__(self, driver, unique_element_id, **kwargs):
        super().__init__(driver, unique_element_id, **kwargs)
        self.elements = [TextInputElementManager(self.driver,
                                                 text='Перечислите награды и достижения вашей организации (рус)',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild',
                                                                 'nextSibling', 'firstChild'],
                                                 set_value="Achievements"),
                         TextInputElementManager(self.driver,
                                                 text='Перечислите награды и достижения вашей организации (англ.)',
                                                 relation_chain=['nextSibling', 'firstChild', 'firstChild',
                                                                 'firstChild',
                                                                 'nextSibling', 'firstChild'], set_value="4755mmr")]
        self.goto_exchange_program_page = ButtonElementManager(self.driver, text="Достижения", wait_limit_sec=3)

    def _update(self) -> None:
        pass

    def _check_update(self) -> None:
        pass

    def _clean(self) -> None:
        pass

    def _check_clean(self) -> None:
        pass

    def _delete(self) -> None:
        pass

    def _check_delete(self) -> None:
        pass
