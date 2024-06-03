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


def get_all_color_modes_information(monitor_id: str):
    """Get information about all color modes for a given monitor.

    URI: '/monitors/{monitor_id}/color-modes'
    Method: GET

    This function sends an HTTP GET request to the specified URI and retrieves
    information about all color modes for the given monitor. If successful,
    it returns a list containing a dictionary with color mode data.
    If an error occurs, an empty list is returned.

    Args:
        monitor_id (str): Identifier of the monitor.

    Returns:
        list [dict]: A list of dictionaries containing color mode information.
        Each dictionary includes the following keys:
        - "selected" (bool): Whether the color mode is currently selected.
        - "enabled" (bool): Whether the color mode is enabled.
        - "index" (bool): Index of the color mode.
        - "name" (str): Name of the color mode
        - "type" (str): Color mode type of the color mode.
        - "target" (dict): A calibration target of Advanced type color mode.
        - "parameters" (dict): The parameters of a Standard or SyncSignal
        type color mode.
    """
    url = BASE_URL + '/monitors/' + monitor_id + '/color-modes'
    result = []

    try:
        with urlopen(url) as response:
            if response.status == 200:
                response_body = json.loads(response.read())
                result = response_body['colorModes']
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

        # Get all color modes information
        color_modes_information = get_all_color_modes_information(
            monitor_id=monitor_id
        )

        if color_modes_information:
            for index, mode in enumerate(color_modes_information):
                print(f'Color mode {index} information:')
                pprint(mode)
                print('')
        else:
            print('Failed to get all color mode information.')
    else:
        print('No monitor found.')
