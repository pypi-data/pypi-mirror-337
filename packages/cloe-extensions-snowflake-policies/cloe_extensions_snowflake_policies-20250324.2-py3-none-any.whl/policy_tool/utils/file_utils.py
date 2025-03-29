import errno
import json
import logging
import os
from typing import Any, Union

import jsonschema

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
        except Exception:
            try:
                encoding = "utf-8"
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except Exception:
                try:
                    encoding = "utf-16-le"
                    with open(file_path, "r", encoding=encoding) as file:
                        return file.read()
                except Exception:
                    try:
                        encoding = "utf-16"
                        with open(file_path, "r", encoding=encoding) as file:
                            return file.read()
                    except Exception:
                        try:
                            encoding = "cp1252"
                            with open(file_path, "r", encoding=encoding) as file:
                                return file.read()
                        except Exception:
                            raise EnvironmentError(
                                f"Can not read file {file_path}. Tried utf-8-sig (BOM), utf-8, utf-16, utf-16-le and cp1252."
                            )


def load_json(
    file_path: str, encoding: str = "utf-8-sig"
) -> Union[dict[str, Any], None]:
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
        raise ValueError(
            f"The file {file_path} is empty and can't be loaded in JSON format."
        )


def validate_json(
    schema_file: str, data_file: str, schema_path_resolver: str = ""
) -> bool:
    """
        Validates a JSON file against a given schema file.
    Args:
        schema_file: absolute file path to a JSON schema
        data_file: relative file path to a JSON file
        schema_path_resolver: absolute folder path to the JSON schema - optional and needed for schema references in complex schemas
    Returns:
        boolean: True is successful, False if failed
    """
    schema = load_json(schema_file)

    data = load_json(data_file)

    if schema_path_resolver and schema:
        base_uri = "file:///{0}/".format(schema_path_resolver)
        resolver = jsonschema.RefResolver(base_uri, schema)

    try:
        if schema_path_resolver and schema:
            jsonschema.validate(data, schema, resolver=resolver)
        elif schema:
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


def save_file(
    output_path: str,
    output_folder_name: str,
    output_file_name: str,
    output_data: Union[str, dict],
) -> str:
    """Save output data to a file. Required output data type is str or dict.

    Args:
        output_path (str): path to the output folder
        output_folder_name (str): output folder name
        output_file_name (str): output file name
        output_data (Union[str, dict]): output data
    """
    if output_path:
        output_folder_path = os.path.join(
            output_path,
            output_folder_name,
        )
        output_file_path = os.path.join(
            output_folder_path,
            output_file_name,
        )

        os.makedirs(output_folder_path, exist_ok=True)

        with open(output_file_path, "w") as f:
            if isinstance(output_data, str):
                f.write(output_data)
            elif isinstance(output_data, dict):
                json.dump(
                    output_data,
                    f,
                    indent=4,
                )
            else:
                raise ValueError(
                    f"Data type {type(output_data).__name__} not supported while trying to save output_data."
                )
    else:
        log.info("No output_path defined! Output is not saved to a file.")
    return output_file_path
