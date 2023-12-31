import os
import subprocess
import json
from utils.html_handler import process_logs_and_generate_html


#   this prototype of the future view triggering tests should include the report html-file in its response.
#   The html file has to be generated on the fly and be self-contained: all images have to be embedded in it.
#   Do not save the file on HD - create it as a ByteIO stream.
#   The html file has to be a merge of all the logs generated by the separate tests that were run.
#   The names of the run tests may be collected by first running pytest in the dry-run mode (or "collectonly" mode).
#   The report has to be assembled synchronously after all tests finish execution.

# TODO: abstract out the logic that discovers test names, include an argument in the created method to
#  return log names or test module names.
#  Create prototype function for two requests:
#  1. To run tests and generate a combined log of all tests. The returned data includes the generated combined log file's name.
#  2. To download the generated combined log file (file name should be included in the request).
#  Read about web applications in general and DRF applications specifically (the backend). You will create one soon.
def run_compound():
    dry_run_command = [
        'pytest',
        '--collectonly'
    ]
    dry_run_result = subprocess.run(dry_run_command, capture_output=True, text=True)
    module_names = []
    for line in dry_run_result.stdout.splitlines():
        module_name_parts = line.strip().split(' ')
        if len(module_name_parts) > 1:
            module_name = module_name_parts[1][:-1]
            if module_name and module_name.endswith('.py'):
                module_names.append(module_name)
    if dry_run_result.returncode == 0:
        command = [
            'pytest',  # Using the Python executable from the app environment
            '-n', '2', *module_names
        ]
        command_result = subprocess.run(command, capture_output=True, text=True)
        # TODO: create config LOGGING_DIR=./logging and inject it into function as a non-default argument
        log_names = [f'logging/{os.path.splitext(x)[0]}.log' for x in module_names]
        if command_result.returncode == 0:
            # Tests ran successfully (though some may have failed)
            return {
                'stdout': command_result.stdout,
                'stderr': command_result.stderr,
                'html': process_logs_and_generate_html(log_names),
                'returncode': command_result.returncode
            }
        else:
            return {
                'stdout': command_result.stdout,
                'stderr': command_result.stderr,
                'returncode': command_result.returncode,
                'message': 'Some tests failed.'
            }


if __name__ == '__main__':
    run_compound()
