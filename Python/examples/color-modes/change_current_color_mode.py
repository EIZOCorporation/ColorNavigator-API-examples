#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def change_current_color_mode(monitor_id: str, color_mode_index: int):
    """Changes current color mode to the specified color mode index.

    URI: '/monitors/{monitor_id}/color-modes/selected-index'
    Method: PUT

    This function sends an HTTP PUT request to the specified URI and change
    current color mode to specified color mode index.

    Args:
        monitor_id (str): Identifier of the monitor.
        color_mode_index (int): The index of the desired color mode (0-based).

    Returns:
        None: Prints a success message if the request is successful.
        Otherwise, print error message.
    """
    url = BASE_URL + '/monitors/' + monitor_id + '/color-modes/selected-index'
    data = {'index': color_mode_index}
    request = Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        method='PUT'
    )
    request.add_header('Content-Type', 'application/json')

    try:
        with urlopen(request) as response:
            if response.status == 200:
                print(
                    'Success to change the color mode index to '
                    + f'{color_mode_index}.'
                )
    except HTTPError as e:
        response_body = json.loads(e.read())
        error_message = response_body['message']
        print(f'Status: {e.code}')
        print(f'Reason: {e.reason}')
        print(f'Message: {error_message}')
    except URLError as e:
        print('Failed to communicate with the ColorNavigator API server.')
        print(f'Reason: {e.reason}')


def get_target_color_mode_index():
    """Prompts the user to input a target color mode index (0 to 9).

    Returns:
        int: The valid color mode index entered by the user.
    """
    while True:
        try:
            color_mode_index = int(
                input('Please input the target color mode index (0 to 9): ')
            )
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

        # Get the information of target color mode index from keyboard input
        color_mode_index = get_target_color_mode_index()

        # Change current color mode to specified index.
        change_current_color_mode(
            monitor_id=monitor_id,
            color_mode_index=color_mode_index
        )
    else:
        print('No monitor found.')
