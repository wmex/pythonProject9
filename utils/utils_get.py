import time
from selenium.common import JavascriptException, TimeoutException

from selenium.webdriver.support.wait import WebDriverWait

from utils.utils_general import execute_js_with_injection
from utils.exceptions import UniveroException


def get_input_or_textarea_elements_values(driver):
    js_code_to_execute = """
    var inputElements = document.querySelectorAll('input, textarea');
    var values = [];
    for (var i = 0; i < inputElements.length; i++) {
        values.push(inputElements[i].value);
    }
    return values;
    """
    try:
        result = execute_js_with_injection(driver, js_code_to_execute)
        return result
    except JavascriptException as e:
        raise UniveroException(
            f'An error occurred while executing JavaScript: {str(e)}'
        )


def count_elements(driver, attribute_name='', attribute_value='', wait_limit_sec=10):

    js_code_to_execute = f"""
    const result = countOfElements("{attribute_name}", "{attribute_value}");
    return result;
    """
    try:
        time.sleep(1)
        result = execute_js_with_injection(driver, js_code_to_execute)
        return result
    except JavascriptException as e:
        raise UniveroException(
            f'An error occurred while executing JavaScript: {str(e)}'
        )

def get_text_content_of_last_element(driver, attribute_name='', attribute_value=''):
    js_code_to_execute = f"""
    const result = getTextContentOfLastElement('{attribute_name}', '{attribute_value}');
    return result;
    """
    try:
        result = execute_js_with_injection(driver, js_code_to_execute)
        return result
    except JavascriptException as e:
        raise UniveroException(
            f'An error occurred while executing JavaScript: {str(e)}'
        )


def get_element_tag_value(driver, *, id='',
                          relation_chain=[], class_names='', placeholder='',
                          inputmode='', tag_name=''):
    relation_chain_quoted = [f'"{x}"' for x in relation_chain]
    relation_chain_js = f"[{', '.join(relation_chain_quoted)}]"
    js_code_to_execute = f"""
               const id = '{id}';
               const inputmode = '{inputmode}';
               const placeholder = '{placeholder}';
               const relationChain = {relation_chain_js};
               const classNames = '{class_names}';
               const tagName = '{tag_name}';
               const result = getElementTagValue(id, placeholder, inputmode, relationChain, classNames, tagName);
               return result;
               """
    try:
        result = execute_js_with_injection(driver, js_code_to_execute)
        return result
    except JavascriptException as e:
        raise UniveroException(
            f'An error occurred while executing JavaScript: {str(e)}'
        )
