import os.path

import logging
import time
import structlog
from typing import List

from config import get_driver, configure_logger
from utils.utils_general import load_page_fully


class PageLoader:
    def __init__(self, driver):
        self.driver = driver

    def load_page(self, url_to_load, load_n_times: int) -> List[float]:
        """
        Loads a page at url_to_load and returns the loading times in seconds.
        Args:
            load_n_times - the page is loaded this many times (to track loading time dynamics).
        """
        result = []
        for _ in range(load_n_times):
            start_time = time.time()
            load_page_fully(driver=self.driver, url=url_to_load)
            end_time = time.time()

            result.append(end_time - start_time)
        return result


def test_cache_warmup():
    driver = get_driver()
    page_loader = PageLoader(driver)
    filename = 'logging/test_cache_warmup'
    configure_logger(filename)
    logging.basicConfig(filename=filename, level=logging.INFO)
    root_logger = logging.getLogger()
    root_logger.handlers = []
    if os.path.exists(filename):
        os.remove(filename)

    logging.basicConfig(filename=filename, level=logging.INFO)

    logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
    logger_struct = structlog.get_logger()

    # log_messages = []
    # logger = structlog.get_logger()
    # logger.addHandler(html_logger)
    #
    # logging.getLogger('')
    # logging.getLogger(__name__, propagate=False)
    # html_logger.clear_existing_content()
    # html_logger.clean_up_screenshots()
    # COMPLETED: include several pages from one domain (including vue and dashboard pages),
    #  include only the pages that take a visibly long time to load after site deployment
    #  (only cached pages should be included in the list).
    urls = ['https://stage.univero.cc', 'https://stage.univero.cc/dashboard/account/',
            'https://stage.univero.cc/univers', 'https://stage.univero.cc/fair', 'https://stage.univero.cc/aboutus',
            'https://stage.univero.cc/contacts', 'https://stage.univero.cc/dashboard/visa',
            'https://stage.univero.cc/dashboard/news']
    page_load_time_stats = []
    for url in urls:
        for i, load_time in enumerate(page_loader.load_page(url, load_n_times=1)):
            if load_time:
                logger.info(f"Page {url} load time on visit #{i}: {load_time} seconds")
                logger_struct.info(f"Page {url} load time on visit #{i}: {load_time} seconds")
    # html_logger = HTMLHandler(level=logging.INFO, filename='logging/selenium_page_loader_test.html', driver=driver)
    #             html_logger.log_exception(f"<ul>Page {url} load time on visit #{i}: {load_time} seconds<br><ul>",
    #                                       save_screenshot=True)
    #             logger.info(f"Page {url} load time on visit #{i}: {load_time} seconds")
    #
    # html_logger.append_in_html()
    # html_logger.clean_up_screenshots()


# COMPLETED: use HTMLLogger to log events (visited pages and their loading times).
if __name__ == "__main__":
    test_cache_warmup()


