import logging
from typing import Optional

from selenium.common import JavascriptException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from config import DEBUG, LOGGING_LEVEL
from utils.utils_general import execute_js_with_injection, ELEMENT_WAIT_LIMIT_SEC
from utils.exceptions import UniveroException

logging.basicConfig(level=LOGGING_LEVEL)


def click_checkbox(driver, *, label_text='', id='', class_name='', set_value=None, relation_chain=[]):
    if isinstance(set_value, bool):
        js_value = 'true' if set_value else 'false'
    else:
        js_value = str(set_value) if set_value is not None else 'null'
    relation_chain_quoted = [f'"{x}"' for x in relation_chain]
    relation_chain_js = f"[{', '.join(relation_chain_quoted)}]"

    js_code_to_execute = f"""
    const labelText = '{label_text}';
    const classNames = '{class_name}';
    const setValue = {js_value};
    const id = '{id}';
    const relationChain = {relation_chain_js};
    const result = clickCheckbox(labelText, id,classNames, setValue, relationChain);
    return result;
    """

    try:
        result = execute_js_with_injection(driver, js_code_to_execute)
    except JavascriptException as e:
        raise UniveroException(
            f'An error occurred while executing JavaScript: {str(e)}'
        )

    if result:
        raise UniveroException(
            f'Error in JavaScript function: {result}. '
            f'Searching element on page {driver.current_url} failed.'
        )


def _operate_element(
        driver, *, id='', text='', relation_chain: Optional[list] = None, placeholder='',
        class_names: str = '', container_xpath: str = '', wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC,
        operation='', skip_error=False,
        click_until_content_or_url_changes=None
):
    # COMPLETED: set all arguments defaulted to [] like this, adding type hint to those arguments
    if relation_chain is None:
        relation_chain = []
    js_condition_err_msg = ''

    def js_condition_element_found_and_operated_on(driver):
        nonlocal js_condition_err_msg
        relation_chain_quoted = [f'"{x}"' for x in relation_chain]
        relation_chain_js = f"[{', '.join(relation_chain_quoted)}]"
        js_code_to_execute = f"""
        const relationChain = {relation_chain_js};
        let element = filterToFirstElementWithAndLogic({{
            text: '{text}',
            id: '{id}',
            classNames: '{class_names}',
            placeholder: '{placeholder}',
            containerXPath: '{container_xpath}'
        }});
        if (element) {{
            if (!relationChain) {{
                element.{operation}();
                return `Element found and {operation}ed.`;
            }} else {{
                element = getRelatedElement(element, relationChain);
                element.{operation}();
                return `Element found and {operation}ed.`;
            }}
        }} else {{
            throw new Error('Element not found');
        }};
        """

        try:
            execute_js_with_injection(driver, js_code_to_execute)
        except JavascriptException as e:
            js_condition_err_msg = str(e)
            return False
        else:
            return True

    original_page_url = driver.current_url
    original_page_content = driver.page_source

    while True:
        try:
            WebDriverWait(driver, wait_limit_sec).until(js_condition_element_found_and_operated_on)
        except TimeoutException as e:
            element_search_info = dict(label_text=text, class_name=class_names)
            if skip_error != DEBUG:
                logging.warning(
                    f'{operation.capitalize()}ing element on page {driver.current_url} have an error with arguments: {element_search_info}. Javascript error: {js_condition_err_msg}')
                return False
            raise TimeoutError(
                f'{operation.capitalize()}ing element on page {driver.current_url} timed out after {wait_limit_sec} seconds. '
                f'Element info: {element_search_info}.'
                f'JavaScript Error: {js_condition_err_msg}'
            ) from e
        if not click_until_content_or_url_changes:
            break
        if driver.current_url != original_page_url or driver.page_source != original_page_content:
            break


def click_element(
        driver, *, id='', text='', relation_chain=[], placeholder='', container_xpath='',
        class_names: str = '', wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC, click_until_content_or_url_changes=False
):
    return _operate_element(
        driver, id=id, text=text, relation_chain=relation_chain, container_xpath=container_xpath,
        placeholder=placeholder, class_names=class_names, wait_limit_sec=wait_limit_sec,
        click_until_content_or_url_changes=click_until_content_or_url_changes, operation='click'
    )


def focus_element(
        driver, *, id='', text='', placeholder='', class_names: str = '', container_xpath='',
        wait_limit_sec=ELEMENT_WAIT_LIMIT_SEC, click_until_content_or_url_changes=False
):
    return _operate_element(
        driver, id=id, text=text, placeholder=placeholder, class_names=class_names, container_xpath=container_xpath,
        wait_limit_sec=wait_limit_sec, click_until_content_or_url_changes=click_until_content_or_url_changes,
        operation='focus'
    )
