import json
import logging
import jsonschema
import errno
import os

from typing import Union

from policy_tool.utils.logger_utils import LoggingAdapter

logger = logging.getLogger(__name__)
log = LoggingAdapter(logger)

def load_file(file_path: str, encoding: str = "utf-8-sig") -> str:
    """
        Reads and returns the file content of given path.
        Encodings tried in following order:
                utf-8-sig - default
                utf-8
                utf-16-le
                utf-16
                cp1252
    Args:
        file_path: absolute file path to a file
        encoding: specific code page name
    Raises:
        EnvironmentError - if file could not been read with stated encodings
    Returns:
        File content as string representation
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
    else:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                return file.read()
        except:
            try:
                encoding = "utf-8"
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except:
                try:
                    encoding = "utf-16-le"
                    with open(file_path, "r", encoding=encoding) as file:
                        return file.read()
                except:
                    try:
                        encoding = "utf-16"
                        with open(file_path, "r", encoding=encoding) as file:
                            return file.read()
                    except:
                        try:
                            encoding = "cp1252"
                            with open(file_path, "r", encoding=encoding) as file:
                                return file.read()
                        except:
                            raise EnvironmentError(
                                f"Can not read file {file_path}. Tried utf-8-sig (BOM), utf-8, utf-16, utf-16-le and cp1252."
                            )

def load_json(file_path: str, encoding: str = "utf-8-sig") -> Union[dict, None]:
    """
        Reads amd returns a given json file. Content must be in valid JSON Schema.
        Valid JSON Schema should not have any trailing commas.
        Raises an error if the file is empty.
        Encodings tried in following order:
                utf-8-sig - default
                utf-8
                utf-16-le
                utf-16
                cp1252
    Args:
        file_path: absolute file path to a file
        encoding: specific code page name
    Raises:
        EnvironmentError - if file could not been read with stated encodings
    Returns:
        File content as dictionary.
        If the file path does not exists None will be returned.
    """
    file_content = load_file(file_path, encoding)
    if file_content:
        return json.loads(load_file(file_path, encoding))
    else:
        raise ValueError(f"The file {file_path} is empty and can't be loaded in JSON format.")


def validate_json(schema_file: str, data_file: str, schema_path_resolver: str = '') -> bool:
    """
        Validates a JSON file against a given schema file.
    Args:
        schema_file: absolute file path to a JSON schema
        data_file: relative file path to a JSON file
        schema_path_resolver: absolute folder path to the JSON schema - optional and needed for schema references in complex schemas
    Returns:
        boolean: True is sucessful, False if failed
    """
    schema = load_json(schema_file)

    data = load_json(data_file)


    if schema_path_resolver:
        base_uri = 'file:///{0}/'.format(schema_path_resolver)
        resolver = jsonschema.RefResolver(base_uri, schema)

    try:
        if schema_path_resolver:
            jsonschema.validate(data, schema, resolver=resolver)
        else:
            jsonschema.validate(data, schema)
    except jsonschema.ValidationError as err:
        log.error(
            f"FAILED validation JSON [ '{data_file}' ] for SCHEMA [ '{schema_file}' ] \n with ERROR [ '{err.message}' ]"
        )
        return False
    except jsonschema.SchemaError as err:
        log.error(
            f"INVALID json SCHEMA [ '{schema_file}' ] with ERROR [ '{err.message}' ]"
        )
        return False
    return True

