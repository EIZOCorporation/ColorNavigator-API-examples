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


def get_key_lock_setting(monitor_id: str):
    """Get the key lock setting for a given monitor.

    URI: '/monitors/{monitor_id}/key-lock'
    Method: GET

    This function sends an HTTP GET request to the specified URI and retrieves
    the key lock setting for a given monitor.
    If successful, it returns a dictionary with key lock setting.
    If an error occurs, an empty dictionary is returned.

    Args:
        monitor_id (str): Identifier of the monitor.

    Returns:
        dict: A dictionary containing key lock setting.
        Dictionary includes the following keys:
        - "keyLock" (str): Key lock setting. ("OFF" or "MENU" or "ALL")
    """
    url = BASE_URL + '/monitors/' + monitor_id + '/key-lock'
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


if __name__ == '__main__':
    monitors_list = get_connected_monitors()

    if monitors_list:
        # Use No.0 monitor as target monitor.
        monitor_id = monitors_list[0]['id']
        model_name = monitors_list[0]['modelName']
        serial_number = monitors_list[0]['serialNumber']
        print(f'Target monitor: {model_name} ({serial_number})')

        # Get the key lock setting
        key_lock_setting = get_key_lock_setting(monitor_id=monitor_id)

        if key_lock_setting:
            print('Success to get the key lock setting.')
            pprint(key_lock_setting)
        else:
            print('Failed to get the key lock setting.')
    else:
        print('No monitor found.')
