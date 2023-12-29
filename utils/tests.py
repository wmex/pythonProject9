import abc
from abc import ABC


class PersonalAccount:

    def __init__(self, credentials: dict):
        if 'email' not in credentials:
            raise KeyError('Provide email address')
        if 'password' not in credentials:
            raise KeyError(f'Provide password for email {credentials["email"]}')

    def login(self):
        raise NotImplementedError('Login')


class StudentPersonalAccount(PersonalAccount):
    ...

class UniversityPersonalAccount(PersonalAccount):
    ...


class SeleniumTest(ABC):
    def __init__(self):
        self.event_handler = Event()
        self.student_personal_account = StudentPersonalAccount(credentials={...})
        self.university_personal_account = UniversityPersonalAccount(credentials={...})

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError


class FillStudentProfileSeleniumTest(SeleniumTest):
    def __init__(self, test_case):
        super().__init__(test_case)

    def run(self):
        self.student_personal_account.login()
        page_object_manager = StudentProfilePageObjectManager()
        try:
            page_object_manager.clean_student_profile()
            page_object_manager.check_clean_stundent_profile()
            page_object_manager.update_student_profile()
            page_object_manager.check_update_stundent_profile()
        except PageObjectManagerException as e:
            pass
        self.student_personal_account.logout()
        self.university_personal_account.login()


# Page Manager:
def update_student_profile(self):
    # update elements through block manager(s)
    self.save_page()
    self.refresh_page()

def check_update_student_profile(self):
    # check updated elements through block manager(s)
    pass
def create_page(self):
    pass

def prepare_for_test(self):
    pass


# class Event:
#     def __init__(self):
#         self._handlers = []
#
#     def add_handler(self, handler):
#         self._handlers.append(handler)
#
#     def trigger(self, *args, **kwargs):
#         for handler in self._handlers:
#             handler(*args, **kwargs)
