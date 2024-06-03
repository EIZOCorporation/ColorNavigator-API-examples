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


def get_color_mode_information(monitor_id: str, color_mode_index: int):
    """Get information about a specific color mode for a given monitor.

    URI: '/monitors/{monitor_id}/color-modes/{color_mode_index}'
    Method: GET

    This function sends an HTTP GET request to the specified URI and retrives
    information about the color mode at the specified index for the given
    monitor. If successful, it returns a dictionary with color mode data.
    If an error occurs, an empty list is returned.

    Args:
        monitor_id (str): Identifier of the monitor.
        color_mode_index (int): Target color mode index.

    Returns:
        dict: A dictionary containing color mode information.
        Dictionary includes the following keys:
        - "selected" (bool): Whether the color mode is currently selected.
        - "enabled" (bool): Whether the color mode is enabled.
        - "index" (bool): Index of the color mode.
        - "name" (str): Name of the color mode
        - "type" (str): Color mode type of the color mode.
        - "target" (dict): A calibration target of Advanced type color mode.
        - "parameters" (dict): The parameters of a Standard or SyncSignal
        type color mode.
    """
    url = BASE_URL + '/monitors/' + monitor_id + \
        '/color-modes/' + str(color_mode_index)
    result = {}

    try:
        with urlopen(url) as response:
            if response.status == 200:
                result = json.loads(response.read())
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


def get_target_color_mode_index():
    """Prompts the user to input a target color mode index (0 to 9).

    Returns:
        int: The valid color mode index entered by the user.
    """
    while True:
        try:
            color_mode_index = int(input(
                'Please input the target color mode index (0 to 9): '
            ))
            if 0 <= color_mode_index <= 9:
                return color_mode_index
            else:
                print('The entered number is out of the range of 0 to 9.')
        except ValueError:
            print('The input value is not a number.')


if __name__ == '__main__':
    monitors_list = get_connected_monitors()

    if monitors_list:
        # Use No.0 monitor as target monitor.
        monitor_id = monitors_list[0]['id']
        model_name = monitors_list[0]['modelName']
        serial_number = monitors_list[0]['serialNumber']
        print(f'Target monitor: {model_name} ({serial_number})')

        # Get the infromation of target color mode index from keyboard input
        color_mode_index = get_target_color_mode_index()

        # Get specified index color mode information
        color_mode_information = get_color_mode_information(
            monitor_id=monitor_id,
            color_mode_index=color_mode_index
        )

        if color_mode_information:
            print(f'Color mode {color_mode_index} information:')
            pprint(color_mode_information)
            print('')
        else:
            print(
                f'Failed to get color mode {color_mode_index} information.')
    else:
        print('No monitor found.')
