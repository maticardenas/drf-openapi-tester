import logging
from typing import Union

logger = logging.getLogger('openapi_tester')


def fetch_generated_schema(url: str, status_code: Union[str, int], method: str) -> dict:
    """
    Fetches dynamically generated schema.

    :param url: API endpoint URL, str
    :param status_code: Response status code, str
    :param method: HTTP method, str
    :return: dict
    """
    logger.debug('Fetching generated dynamic schema')
    from drf_yasg.openapi import Info
    from drf_yasg.generators import OpenAPISchemaGenerator

    schema = OpenAPISchemaGenerator(info=Info(title='', default_version='')).get_schema()['paths']
    try:
        schema = schema[url]
    except KeyError:
        raise KeyError(f'No path found for url `{url}`. Valid urls include {", ".join([key for key in schema.keys()])}')
    try:
        schema = schema[method.lower()]['responses']
    except KeyError:
        raise KeyError(
            f'No schema found for method {method.upper()}. Available methods include '
            f'{", ".join([method.upper() for method in schema.keys() if method.upper() != "PARAMETERS"])}.'
        )
    try:
        return schema[f'{status_code}']
    except KeyError:
        raise KeyError(
            f'No schema found for response code {status_code}. Documented responses include '
            f'{", ".join([code for code in schema.keys()])}.'
        )