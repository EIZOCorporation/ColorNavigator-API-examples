#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
import os


CN_API_SERVER_ADDRESS = '127.0.0.1'
PORT = '50005'  # change this variable to match your API port settings.
BASE_URL = 'http://' + CN_API_SERVER_ADDRESS + ':' + PORT


# Bypass the proxy for communication with the local ColorNavigator API server
os.environ['NO_PROXY'] = CN_API_SERVER_ADDRESS


class PixelInspectionMarkerState(Enum):
    SHOW = 'SHOW'
    HIDE = 'HIDE'


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


def change_pixel_inspection_marker_state(
    monitor_id: str,
    state: PixelInspectionMarkerState,
    coordinates: tuple[int, int] | None = None,
):
    """Change the cross marker state of pixel inspection at the specified
    coordinate for a given monitor.

    URI: '/monitors/{monitor_id}/pixel-inspection/marker'
    Method: PUT

    This function sends an HTTP Put request to the specified URI and change
    the cross marker state of pixel inspection for a given monitor.
    If 'SHOW' is specified as the state, x_coordinate and y_coordinate data is
    necessary.

    Args:
        monitor_id (str): Identifier of the monitor.
        state (PixelInspectionMarkerState): The marker state.
        ('SHOW' or 'HIDE')
        coordinates (tuple[int, int], optional): X and Y coordinates of
        the target pixel. Required when state is 'SHOW' (None is not allowed).

    Returns:
        None: Prints a success message if the request is successful.
        Otherwise, print error message.
    """
    url = BASE_URL + '/monitors/' + monitor_id + '/pixel-inspection/marker'
    data = {'marker': state.value}

    if state == PixelInspectionMarkerState.SHOW:
        data['position'] = {'x': coordinates[0], 'y': coordinates[1]}

    request = Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        method='PUT'
    )
    request.add_header('Content-Type', 'application/json')

    try:
        with urlopen(request) as response:
            if response.status == 204:
                if state == PixelInspectionMarkerState.SHOW:
                    print('Success to show the cross marker at ', end='')
                    print(f'({coordinates[0]}, {coordinates[1]}).')
                else:
                    print('Success to hide the cross marker.')
    except HTTPError as e:
        response_body = json.loads(e.read())
        error_message = response_body['message']
        print(f'Status: {e.code}')
        print(f'Reason: {e.reason}')
        print(f'Message: {error_message}')
    except URLError as e:
        print('Failed to communicate with the ColorNavigator API server.')
        print(f'Reason: {e.reason}')


def get_target_pixel_coordinates():
    """Prompts the user to input the x and y coordinate information of
    target pixel.

    Returns:
        tuple[int, int]: A tuple which contains x and y coordinate
        information of target pixel.
    """
    while True:
        try:
            x_coordinate = int(
                input('Please input the x coordinate of target pixel: ')
            )
            y_coordinate = int(
                input('Please input the y coordinate of target pixel: ')
            )
            return x_coordinate, y_coordinate
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

        # Show the cross market at the specified coordinate.
        change_pixel_inspection_marker_state(
            monitor_id=monitor_id,
            state=PixelInspectionMarkerState.SHOW,
            coordinates=get_target_pixel_coordinates(),
        )

        # after 3s, hide the cross marker
        sleep(3)
        change_pixel_inspection_marker_state(
            monitor_id=monitor_id,
            state=PixelInspectionMarkerState.HIDE
        )
    else:
        print('No monitor found.')
