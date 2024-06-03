#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
import os


CN_API_SERVER_ADDRESS = '127.0.0.1'
PORT = '50005'  # change this variable to match your API port settings.
BASE_URL = 'http://' + CN_API_SERVER_ADDRESS + ':' + PORT


# Bypass the proxy for communication with the local ColorNavigator API server
os.environ['NO_PROXY'] = CN_API_SERVER_ADDRESS


def get_connected_monitors():
    """Get connected monitors list.

    URI: '/monitors'
    Method: GET

    This function sends an HTTP GET request to the specified URI and retrieves
    information about connected monitors. If successful, it returns a list of
    dictionaries containing monitor data. If no monitors are found or if an
    error occurs, an empty list is returned.

    Returns:
        list [dict]: A list of dictionaries containing monitor information.
        Each dictionary includes the following keys:
        - "id" (str): The unique identifier for the monitor.
        - "modelName" (str): The model name of the monitor.
        - "serialNumber" (str): The serial number of the monitor.
    """
    url = BASE_URL + '/monitors'
    result = []

    try:
        with urlopen(url) as response:
            if response.status == 200:
                response_body = json.loads(response.read())
                result = response_body['monitors']
    except HTTPError as e:
        response_body = json.loads(e.read())
        error_message = response_body['message']
        print(f'Status: {e.code}')
        print(f'Reason: {e.reason}')
        print(f'Message: {error_message}')
    except URLError as e:
        print('Failed to communicate with the ColorNavigator API server.')
        print(f'Reason: {e.reason}')
    finally:
        return result


def create_calibration_target(
        monitor_id: str,
        settings: dict):
    """Create a new calibration target with the provided settings values.

    URI: '/monitors/{monitor_id}/targets'
    Method: POST

    This function sends an HTTP POST request to the specified URI and
    create a new calibration target for the given monitor based on
    the provided settings.

    Args:
        monitor_id (str): Identifier of the monitor.
        settings (dict): A dictionary containing the target settings.

    Returns:
        None: Prints a success message if the request is successful.
        Otherwise, print error message.
    """
    url = BASE_URL + '/monitors/' + monitor_id + '/targets'
    request = Request(
        url,
        data=json.dumps(settings).encode('utf-8'),
        method='POST'
    )
    request.add_header('Content-Type', 'application/json')

    try:
        with urlopen(request) as response:
            if response.status == 201:
                print('Success to create calibration target.')
    except HTTPError as e:
        response_body = json.loads(e.read())
        error_message = response_body['message']
        print(f'Status: {e.code}')
        print(f'Reason: {e.reason}')
        print(f'Message: {error_message}')
    except URLError as e:
        print('Failed to communicate with the ColorNavigator API server.')
        print(f'Reason: {e.reason}')


if __name__ == '__main__':
    monitors_list = get_connected_monitors()

    if monitors_list:
        # Use No.0 monitor as target monitor.
        monitor_id = monitors_list[0]['id']
        model_name = monitors_list[0]['modelName']
        serial_number = monitors_list[0]['serialNumber']
        print(f'Target monitor: {model_name} ({serial_number})')

        settings = {
            'name': 'API_Target',
            'colorModeName': 'CAL_API',
            'parameters': {
                'brightness': {'type': 'CANDELA', 'value': 100},
                'blackLevel': {'type': 'MIN'},
                'whitePoint': {'type': 'TEMPERATURE', 'value': 6500},
                'gamma': {'type': 'GAMMA', 'value': 2.2},
                'gamut': {
                    'type': 'STANDARD', 'value': 'ADOBE_RGB', 'clipping': False
                },
                'calibrationPolicy': 'GRAY_BALANCE',
                'sixColors': {
                    "red": {"hue": 0, "saturation": 0, "lightness": 0},
                    "green": {"hue": 0, "saturation": 0, "lightness": 0},
                    "blue": {"hue": 0, "saturation": 0, "lightness": 0},
                    "cyan": {"hue": 0, "saturation": 0, "lightness": 0},
                    "magenta": {"hue": 0, "saturation": 0, "lightness": 0},
                    "yellow": {"hue": 0, "saturation": 0, "lightness": 0}
                },
                'optimizeForLimited109': False
            },
            'profileUpdateRule': 'EVERYTIME',
            'profilePolicy': {
                'profileVersion': "4.2",
                'toneCurve': 'LUT',
                'reflectBlackLevel': True
            },
            'useTargetNameAsProfileName': False,
            'protection': False
        }

        print('Create a new calibration target with the following content.')
        pprint(settings)
        create_calibration_target(
            monitor_id=monitor_id,
            settings=settings
        )
    else:
        print('No monitor found.')
