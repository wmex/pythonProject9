import structlog
import json
import io

class HTMLLogFormatter:
    def __call__(self, logger, method_name, event_dict):
        timestamp = event_dict.get("timestamp", "")
        level = event_dict.get("level", "")
        message = event_dict.get("msg", "")

        html_message = f"<p><strong>{timestamp} [{level}]</strong>: {message}</p>"
        event_dict["html_message"] = html_message

        return event_dict

def process_logs_and_generate_html(log_files):
    logger = structlog.get_logger()
    logger = logger.bind(html_formatter=HTMLLogFormatter())

    with io.BytesIO() as bytes_io_handler:
        for log_file_path in log_files:
            with open(log_file_path, "r") as log_file:
                log_entries = log_file.read()
                bytes_io_handler.write(log_entries.encode("utf-8"))

    # Access the HTML content from the custom BytesIOHandler
    html_content = bytes_io_handler.getvalue().decode("utf-8")
    # TODO: debug with logger.info and logger.level='INFO' in development
    #  better: read how to suppress dependencies' DEBUG-level logs and use logger.debug in development
    print(html_content)
    return html_content
