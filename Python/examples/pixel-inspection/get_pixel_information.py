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


def get_pixel_information(
        monitor_id: str,
        coordinates: tuple[int, int],
        show_marker: bool):
    """Get pixel information of specified coordinate for a given monitor.

    URI: '/monitors/{monitor_id}/pixel-inspection'
    Method: GET

    This function sends an HTTP GET request to the specified URI and retrieves
    pixel information of specified coordinate for a given monitor.
    If successful, it returns a dictionary with pixel information.
    If an error occurs, an empty dictionary is returned.

    Args:
        monitor_id (str): Identifier of the monitor.
        coordinates (tuple[int, int]): X and Y coordinates of the target pixel.
        show_marker (bool): Whether display the cross marker
        at the target pixel.

    Returns:
        dict: A dictionary containing pixel information.
        Dictionary includes the following keys:
        - "colorFormat" (str): Color format information of current signal.
        ("RGB" or "YCBCR")
        - "hdcp" (bool): HDCP authentication status of current input port.
        - "position" (dict): The coordinate information specified when
        obtaining pixel information.
        - "rawValue" (dict): Each color value that monitor received
        as input signal.
        - "convertedRgbFull" (dict): Actual color value displayed
        on the monitor.
    """
    url = BASE_URL + '/monitors/' + monitor_id + '/pixel-inspection'
    query = '?x=' + str(coordinates[0]) + '&y=' + str(coordinates[1]) + \
        '&show-marker=' + str(show_marker).lower()
    result = {}

    try:
        with urlopen(url + query) as response:
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


def get_target_pixel_coordinates():
    """Prompts the user to input the x and y coorinate information of
    target pixel.

    Returns:
        tuple[int, int]: A tuple which contains x and y coorinate
        information of target pixel.
    """
    while True:
        try:
            x_coordinate = int(input(
                'Please input the x coorinate information of target pixel: '
            ))
            y_coordinate = int(input(
                'Please input the y coorinate information of target pixel: '
            ))
            return x_coordinate, y_coordinate
        except ValueError:
            print('The input value is not a number.')


def confirm_show_marker():
    """Prompts the user to input 'Yes' or 'No' and converts the response
    to a boolean value.

    Returns:
        bool: True if the user inputs 'Yes', False if 'No'.
    """
    yes_no_dict = {'y': True, 'yes': True, 'n': False, 'no': False}
    while True:
        print(
            'Do you want to show the cross marker at the target pixel? ',
            end='')
        choice = input('[Y]es/[N]o: ').lower()

        if choice in yes_no_dict:
            return yes_no_dict[choice]
        else:
            print('Please input [Y]es/[N]o.')


if __name__ == '__main__':
    monitors_list = get_connected_monitors()

    if monitors_list:
        # Use No.0 monitor as target monitor.
        monitor_id = monitors_list[0]['id']
        model_name = monitors_list[0]['modelName']
        serial_number = monitors_list[0]['serialNumber']
        print(f'Target monitor: {model_name} ({serial_number})')

        # Get the specified coordinate pixel information
        pixel_information = get_pixel_information(
            monitor_id=monitor_id,
            coordinates=get_target_pixel_coordinates(),
            show_marker=confirm_show_marker()
        )

        if pixel_information:
            print('Success to get the pixel information.')
            pprint(pixel_information)
        else:
            print('Failed to get the pixel information.')
    else:
        print('No monitor found.')
