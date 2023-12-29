from typing import Optional

from selenium.common import JavascriptException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from utils.utils_general import execute_js_with_injection, ELEMENT_WAIT_LIMIT_SEC
from utils.exceptions import UniveroException


# COMPLETED: check success
def set_first_input_field_by_send_keys_js(
        driver, *, id='',
        relation_chain=[], class_names='', placeholder='',
        inputmode='', inputmode_content='', text='', container_xpath='', set_value=None, wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC):
    return _operate_input_field(
        driver, id=id, relation_chain=relation_chain, class_names=class_names,
        placeholder=placeholder, inputmode=inputmode, inputmode_content=inputmode_content, text=text,
        set_value=set_value, wait_limit_sec=wait_limit_sec, container_xpath=container_xpath,
        operation='setElementValueBySendKeys'
    )


def _operate_input_field(driver, *, id='',
                         relation_chain: Optional[list] = None, class_names='', placeholder='',
                         inputmode='', text='', inputmode_content='', set_value=None,
                         wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC, container_xpath, operation=''):
    js_condition_err_msg = ''
    if relation_chain is None:
        relation_chain = []

    def js_condition(driver):
        nonlocal js_condition_err_msg
        relation_chain_quoted = [f'"{x}"' for x in relation_chain]
        relation_chain_js = f"[{', '.join(relation_chain_quoted)}]"
        js_code_to_execute = f"""
           const id = '{id}';
           const inputmode = '{inputmode}';
           const placeholder = '{placeholder}';
           const labelText = '{text}';
           const valueToSet = '{set_value}';
           const relationChain = {relation_chain_js};
           const classNames = '{class_names}';
           const inputmodeContent = '{inputmode_content}';
           const containerXPath = '{container_xpath}';
           const result = {operation}(labelText, placeholder, id, inputmode, relationChain, classNames, valueToSet, inputmodeContent, containerXPath);
           if (result) {{
               return result;
           }}
           else {{
               return false;
           }}
           """
        try:
            execute_js_with_injection(driver, js_code_to_execute)
        except JavascriptException as e:
            js_condition_err_msg = str(e)
            return False
        else:
            return True

    try:
        WebDriverWait(driver, wait_limit_sec).until(js_condition)
    except TimeoutException:
        element_search_info = dict(label_text=text, class_names=class_names, placeholder=placeholder, id=id)
        raise TimeoutError(
            f'Setting element on page {driver.current_url} timed out after {wait_limit_sec} seconds. '
            f'Element info: {element_search_info}.'
            f'JavaScript error message: {js_condition_err_msg}'
        )


def check_first_input_field(driver, *, id='',
                            relation_chain: Optional[list] = None, class_names='', placeholder='',
                            inputmode='', text='', check_value=None, inputmode_content='', wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC):
    js_condition_err_msg = ''
    if relation_chain is None:
        relation_chain = []

    relation_chain_quoted = [f'"{x}"' for x in relation_chain]
    relation_chain_js = f"[{', '.join(relation_chain_quoted)}]"
    js_code_to_execute = f"""
               const id = '{id}';
               const inputmode = '{inputmode}';
               const placeholder = '{placeholder}';
               const labelText = '{text}';
               const valueToCheck = '{check_value}';
               const relationChain = {relation_chain_js};
               const classNames = '{class_names}';
               const result = checkElementValue(labelText, placeholder, id, inputmode, relationChain, classNames, valueToCheck);
               if (result) {{
                   return result;
               }}
               else {{
                   return false;
               }}
               """
    try:
        result = execute_js_with_injection(driver, js_code_to_execute)
        return result
    except JavascriptException as e:
        return False


def set_file_to_input_field(driver, *, file_path='', id='', class_names='', text='',
                            relation_chain: Optional[list] = None,
                            placeholder='', inputmode=''):
    if relation_chain is None:
        relation_chain = []
    relation_chain_quoted = [f'"{x}"' for x in relation_chain]
    relation_chain_js = f"[{', '.join(relation_chain_quoted)}]"
    js_code_to_execute = f"""
    const labelText = '{text}';
    const id = '{id}';
    const placeholder = '{placeholder}';
    const inputmode = '{inputmode}';
    const filePath ='{file_path}';
    const classNames = '{class_names}';
    const relationChain = {relation_chain_js}
    submitFile(labelText, placeholder, id, inputmode, relationChain, classNames, filePath);"""

    try:
        execute_js_with_injection(driver, js_code_to_execute)
    except JavascriptException as e:
        raise UniveroException(
            f'An error occurred while executing JavaScript: {str(e)}'
        )


def find_element_and_send_keys(driver, *, id='', class_names='', placeholder='',
                               inputmode='', text='', keys='', wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC):
    js_condition_err_msg = ''

    def js_condition(driver):
        nonlocal js_condition_err_msg
        js_code_to_execute = f"""
           const id = '{id}';
           const inputmode = '{inputmode}';
           const placeholder = '{placeholder}';
           const labelText = '{text}';
           const keys = '{keys}';
           const classNames = '{class_names}';
           const result = sendKeysToElement(labelText, placeholder, id, inputmode, classNames, keys);
           if (result) {{
               return result;
           }}
           else {{
               return false;
           }}
           """
        try:
            execute_js_with_injection(driver, js_code_to_execute)
        except JavascriptException as e:
            js_condition_err_msg = str(e)
            return False
        else:
            return True

    try:
        WebDriverWait(driver, wait_limit_sec).until(js_condition)
    except TimeoutException:
        element_search_info = dict(label_text=text, class_names=class_names, placeholder=placeholder, id=id)
        raise TimeoutError(
            f'Setting element on page {driver.current_url} timed out after {wait_limit_sec} seconds. '
            f'Element info: {element_search_info}.'
            f'JavaScript error message: {js_condition_err_msg}'
        )


def find_element_by_input_value_and_click(driver, *, value='', relation_chain=[]):
    relation_chain_quoted = [f'"{x}"' for x in relation_chain]
    relation_chain_js = f"[{', '.join(relation_chain_quoted)}]"
    js_code_to_execute = f"""
    const relationChain = {relation_chain_js};
    let element = findInputElementByValue('{value}')
    element = getRelatedElement(element, relationChain);
    element.click();
    """
    try:
        execute_js_with_injection(driver, js_code_to_execute)
    except JavascriptException as e:
        raise UniveroException(
            f'An error occurred while executing JavaScript: {str(e)}'
        )

# def check_existence_of_element_by_value(driver, *, value=''):
#     js_code_to_execute = f"""
#     checkExistenceOfElementByValue('{value}')
#     """
#     try:
#         result = execute_js_with_injection(driver, js_code_to_execute)
#         return result
#     except JavascriptException as e:
#         raise UniveroException(
#             f'An error occurred while executing JavaScript: {str(e)}'
#         )
