#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
import os


CN_API_SERVER_ADDRESS = '127.0.0.1'
PORT = '50005'  # change this variable to match your API port settings.
BASE_URL = 'http://' + CN_API_SERVER_ADDRESS + ':' + PORT


# Bypass the proxy for communication with the local ColorNavigator API server
os.environ['NO_PROXY'] = CN_API_SERVER_ADDRESS


class KeyLockSetting(Enum):
    OFF = 'OFF'
    MENU = 'MENU'
    ALL = 'ALL'

    @classmethod
    def has(cls, value):
        for member in cls:
            if member.value == value:
                return True
        return False


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


def change_key_lock_setting(
        monitor_id: str,
        key_lock_setting: KeyLockSetting):
    """Change the key lock setting for a given monitor.

    URI: '/monitors/{monitor_id}/key-lock'
    Method: PUT

    This function sends an HTTP PUT request to the specified URI and change
    the key lock setting for the given monitor.

    Args:
        monitor_id (str): Identifier of the monitor.
        key_lock_setting (KeyLockSetting): KeyLockSetting.
        ('OFF' or 'MENU' or 'ALL')

    Returns:
        None: Prints a success message if the request is successful.
        Otherwise, print error message.
    """
    url = BASE_URL + '/monitors/' + monitor_id + '/key-lock'
    data = {'keyLock': key_lock_setting.value}
    request = Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        method='PUT'
    )
    request.add_header('Content-Type', 'application/json')

    try:
        with urlopen(request) as response:
            if response.status == 204:
                print('Success to change the key lock setting to ' +
                      f'"{key_lock_setting.value}".')
    except HTTPError as e:
        response_body = json.loads(e.read())
        error_message = response_body['message']
        print(f'Status: {e.code}')
        print(f'Reason: {e.reason}')
        print(f'Message: {error_message}')
    except URLError as e:
        print('Failed to communicate with the ColorNavigator API server.')
        print(f'Reason: {e.reason}')


def get_key_lock_setting_str():
    """Prompts the user to input 'OFF' or 'MENU' or 'ALL'.

    Returns:
        KeyLockSetting: Key lock setting.
    """
    while True:
        print('Please input key lock setting. ', end='')
        setting = input('[OFF]/[MENU]/[ALL]: ').upper()

        if KeyLockSetting.has(setting):
            return KeyLockSetting(setting)
        else:
            print('Specified key lock setting is invalid.')


if __name__ == '__main__':
    monitors_list = get_connected_monitors()

    if monitors_list:
        # Use No.0 monitor as target monitor.
        monitor_id = monitors_list[0]['id']
        model_name = monitors_list[0]['modelName']
        serial_number = monitors_list[0]['serialNumber']
        print(f'Target monitor: {model_name} ({serial_number})')

        # Change key lock setting with specified setting.
        change_key_lock_setting(
            monitor_id=monitor_id,
            key_lock_setting=get_key_lock_setting_str()
        )
    else:
        print('No monitor found.')
