import logging
import os, sys
import datetime
import time

current_working_dir = os.getcwd()
sys.path.append(current_working_dir)

import setup
from policy_tool import main
from policy_tool.utils.logger_utils import LoggingAdapter

########################################################################################################################
# configure login

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("policytool")
logger.setLevel(logging.INFO)
log = LoggingAdapter(logger)

logging.getLogger("snowflake.connector").setLevel(logging.WARNING)

########################################################################################################################
########################################################################################################################

setup.setup()

fetch_pipeline = False
dryrun_pipeline = True
policy_pipeline = True

########################################################################################################################
### fetch pipeline
if fetch_pipeline:
    log.info(f'============= Start time fetch pipeline {datetime.datetime.now().strftime("%Y-%m-%d__%H:%M:%S")}')
    start_time_fetch_pipeline = time.time()

    # fetch assignments job
    main.fetch_policy_assignments(output_path='examples/example1/output/fetch_output/',
        policy_assignments_jsonschema_relative_path='../../../../json-schemas/policy_assignments.schema.json')

    # fetch policy objects job
    main.fetch_policy_objects()

    end_time_fetch_pipeline = time.time()
    log.info(f'============= Execution time fetch pipeline {round(end_time_fetch_pipeline-start_time_fetch_pipeline,2)}')
########################################################################################################################
### dry-run pipeline
if dryrun_pipeline:
    log.info(f'============= Start time dry-run pipeline {datetime.datetime.now().strftime("%Y-%m-%d__%H:%M:%S")}')
    start_time_dryrun_pipeline = time.time()

    # technical validation job
    main.validate_technical()

    # content validation job
    main.validate_content()

    # assign policies job
    main.validate_technical()
    main.execute_policy_assignments(dryrun=True, output_sql_statements=True, output_path='examples/example1/output/execute_policy_assignments_sql_output/')

    end_time_dryrun_pipeline = time.time()
    log.info(f'============= Execution time dry-run pipeline {round(end_time_dryrun_pipeline-start_time_dryrun_pipeline,2)}')
########################################################################################################################
### policy pipeline
if policy_pipeline:
    log.info(f'============= Start time policy pipeline {datetime.datetime.now().strftime("%Y-%m-%d__%H:%M:%S")}')
    start_time_policy_pipeline = time.time()

    # technical validation job
    main.validate_technical()

    # content validation job
    main.validate_content()

    # assign policies job
    main.validate_technical()
    main.execute_policy_assignments(output_sql_statements=True, output_path='examples/example1/output/execute_policy_assignments_sql_output/')

    end_time_policy_pipeline = time.time()
    log.info(f'============= Execution time policy pipeline {round(end_time_policy_pipeline - start_time_policy_pipeline,2)}')
########################################################################################################################