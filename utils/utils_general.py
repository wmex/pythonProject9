import os
import secrets
import string
import subprocess
import sys
from collections import namedtuple

import psutil
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

ElementInfo = namedtuple('ElementInfo', ['page_url', 'description', 'xpath'])

load_dotenv()

ELEMENT_WAIT_LIMIT_SEC = int(os.environ.get('ELEMENT_WAIT_LIMIT_SEC'))


def str2bool(value):
    if value is None:
        return None
    elif isinstance(value, bool):
        return value
    elif isinstance(value, str):
        value = value.strip().lower()
        if value in ('true', 'yes', 'on', '1'):
            return True
        elif value in ('false', 'no', 'off', '0'):
            return False
        else:
            return None
    else:
        return None


def execute_js_with_injection(driver, js_code_to_execute, injection_file='js_injection_funcs.js'):
    injection_file_path = injection_file
    with open(injection_file_path, 'r', encoding='utf-8') as f:
        js_functions = f.read()
    full_script = js_functions + '\n' + js_code_to_execute

    # This block is for debugging JavaScript. The printed code is runnable in a browser's developer tools' console,
    # if return statements at the bottom are replaced with console.log statements.

    # if 'welcome-find-button' in full_script:
    #     print(full_script)
    #     pdb.set_trace()

    return driver.execute_script(full_script)


def is_chrome_running():
    try:
        for process in psutil.process_iter(attrs=['name']):
            process_name = process.info['name'].lower()
            if 'chrome' in process_name or 'chromium' in process_name:
                return True
        return False
    except Exception as e:
        print(f"An error occurred while checking for Chrome processes: {e}")
        return False


def run_chrome_if_needed(chrome_path: str):
    from config import DEBUG
    if not DEBUG:
        return

    if is_chrome_running():
        print("Chrome is already running, skipping running another instance.")
        return

    cmd = [
        chrome_path,
        "--remote-debugging-port=9222",
        "--start-maximized"
    ]

    platform = sys.platform
    if platform == "win32":
        subprocess.Popen(cmd, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    elif platform == "darwin":  # macOS
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    else:  # Linux and other Unix-like
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                         start_new_session=True)

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


# TODO: use this function to wait for pages to fully load
#  EXPECTED RESUlT DOESNT MATCH WITH REAL RESULT
def load_page_fully(driver, url, timeout_secs=10, loading_element_selector=".loading"):
    driver.get(url)

    # Wait for the readyState to be complete
    WebDriverWait(driver, timeout_secs).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

    # Wait for AJAX calls to complete (jQuery example)
    # Note: Only include this line if the website uses jQuery for AJAX calls.
    # WebDriverWait(driver, timeout_secs).until(
    #     lambda d: d.execute_script('return jQuery.active == 0')
    # )

    # Wait for the absence of the loading indicator
    WebDriverWait(driver, timeout_secs).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, loading_element_selector))
    )
