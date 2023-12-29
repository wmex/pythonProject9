import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from utils.utils_general import str2bool
import structlog
load_dotenv()
DRIVER_SERVICE = os.getenv('DRIVER_SERVICE')
BASE_DASHBOARD_URL = os.getenv('BASE_DASHBOARD_URL')
BASE_VUE_URL = os.getenv('BASE_VUE_URL')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
STUDENT_EMAIL = os.getenv('STUDENT_EMAIL')
STUDENT_PASSWORD = os.getenv('STUDENT_PASSWORD')
UNIVERSITY_EMAIL = os.getenv('UNIVERSITY_EMAIL')
UNIVERSITY_PASSWORD = os.getenv('UNIVERSITY_PASSWORD')
PREORDER_TO_EMAIL_EMAIL = os.getenv('PREORDER_TO_EMAIL_EMAIL')
PREORDER_TO_EMAIL_PASSWORD = os.getenv('PREORDER_TO_EMAIL_PASSWORD')
BITRIX_EMAIL = os.getenv('BITRIX_EMAIL')
BITRIX_PASSWORD = os.getenv('BITRIX_PASSWORD')
CHROME_PATH = os.getenv('CHROME_PATH')

# This allows the WebDriver to connect to the debugging port and automate the browser remotely.
remote_debugging_port = "9222"  # You need to start Chromium with this port
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
#chrome_options.add_argument("--enable-local-storage")
#chrome_options.add_argument("--user-data-dir=/path/to/custom/profile")
DEBUG = str2bool(os.environ.get('DEBUG'))
if DEBUG:
    LOGGING_LEVEL = 'WARNING'
    chrome_options.add_experimental_option(
        'debuggerAddress', f'localhost:{remote_debugging_port}')
else:
    LOGGING_LEVEL = 'ERROR'


def get_driver() -> WebDriver:
    driver_service = Service(executable_path=DRIVER_SERVICE)
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    return driver


def set_process_id(_, __, event_dict):
    event_dict["process_id"] = os.getpid()
    return event_dict


def configure_logger(filename):
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            set_process_id,
            structlog.processors.EventRenamer("msg"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.WriteLoggerFactory(
            file=Path(filename).with_suffix(".log").open("wt")
        ),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO)
    )
# Configuration for setting default level of logging, instead of INFO can pass any level
# structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.INFO))

# class CustomPrintLogger:
#     def msg(self, message):
#         print(message)
# def proc(logger, method_name, event_dict):
#     print("I got called with", event_dict)
#     return repr(event_dict)
# # Wrapping logger manually using structlog
# log = structlog.wrap_logger(
#     CustomPrintLogger(),
#     wrapper_class=structlog.BoundLogger,
#     processors=[proc],
# )
TEXT_TO_CLEAR_MAX_LENGTH = 100
