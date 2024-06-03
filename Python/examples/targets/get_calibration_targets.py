#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
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


def get_calibration_targets(monitor_id: str):
    """Get information about calibration targets for a given monitor.

    URI: '/monitors/{monitor_id}/targets'
    Method: GET

    This function sends an HTTP GET request to the specified URI and retrieves
    information about calibration targets for the given monitor. If successful,
    it returns a list containing a dictionary with target data.
    If an error occurs, an empty list is returned.

    Args:
        monitor_id (str): Identifier of the monitor.

    Returns:
        list [dict]: A list of dictionaries containing target information.
        Each dictionary includes the following keys:
        - "id" (str): An identifier of the target.
        - "name" (str): A name of the target.
        - "colorModeName" (str): A color mode name associated with the target.
        - "parameters" (dict): Each parameter of the target.
        - "profileUpdateRule" (str): A new ICC profile creation rule.
        ("EVERYTIME" or "CONCRETE")
        - "profilePolicy" (dict): A creation policy of the ICC profile.
        - "useTargetNameAsProfileName" (bool): Whether the target name is used
        in the ICC profile name.
        - "protection" (bool): Whether the target can be edited/deleted.
    """
    url = BASE_URL + '/monitors/' + monitor_id + '/targets'
    result = []

    try:
        with urlopen(url) as response:
            if response.status == 200:
                response_body = json.loads(response.read())
                result = response_body['targets']
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


if __name__ == '__main__':
    monitors_list = get_connected_monitors()

    if monitors_list:
        # Use No.0 monitor as target monitor.
        monitor_id = monitors_list[0]['id']
        model_name = monitors_list[0]['modelName']
        serial_number = monitors_list[0]['serialNumber']
        print(f'Target monitor: {model_name} ({serial_number})')

        # Get all calibration targets information
        calibration_targets = get_calibration_targets(
            monitor_id=monitor_id
        )

        if calibration_targets:
            print(f'{len(calibration_targets)} targets were found.')
            for index, mode in enumerate(calibration_targets):
                print(f'Target index: {index + 1}')
                pprint(mode)
                print('')
        else:
            print('Failed to get calibration targets information.')
    else:
        print('No monitor found.')
