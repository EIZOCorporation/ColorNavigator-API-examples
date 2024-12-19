# ColorNavigator API Python Examples

This folder contains example code for using the ColorNavigator API in Python.

## Usage

1. The scripts are organized into subfolders corresponding to different API endpoints for ease of navigation.
2. Choose the appropriate subfolder if necessary, depending on the sample you want to run.

```shell
cd <subfolder_name>
```

3. Run the example code.

```shell
python <example_script.py>
```

4. Customize the example code to fit your specific application needs.

## Details

| API | Example Code | Description |
| :--: | :--: | :--: |
| [`GET /monitors`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/getMonitors) | [get_connected_monitors.py](./examples/get_connected_monitors.py) | Retrieves information about connected monitors. |
| [`GET /monitors/{monitorId}/color-modes`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/getColorModes) | [get_all_color_modes_information.py](./examples/color-modes/get_all_color_modes_information.py) | Retrieves information about all color modes. |
| [`PUT /monitors/{monitorId}/color-modes/selected-index`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/setSelectedColorModeIndex) | [change_current_color_mode.py](./examples/color-modes/change_current_color_mode.py) | Changes current color mode index to specified index. |
| [`GET /monitors/{monitorId}/color-modes/{colorModeIndex}`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/getColotMode) | [get_color_mode_information.py](./examples/color-modes/get_color_mode_information.py) | Retrieves information about the color mode at the specified index. |
| [`PATCH /monitors/{monitorId}/color-modes/{colorModeIndex}`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/updateColotMode) | [change_color_mode_settings.py](./examples/color-modes/change_color_mode_settings.py) | Modifies the settings of the specified color mode index. |
| [`GET /monitors/{monitorId}/color-modes/{colorModeIndex}/target/calibration-results`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/getCalibrationResults) | [get_calibration_results.py](./examples/color-modes/get_calibration_results.py) | Retrieves all calibration result information associated with the calibration target which is applied to the specified index color mode. |
| [`GET /monitors/{monitorId}/color-modes/{colorModeIndex}/target/calibration-results/{calibrationResultId}/validation-results`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/getValidationResults) | [get_validation_results.py](./examples/color-modes/get_validation_results.py) | Retrieves all validation results associated with the calibration result of calibration target which applied to the specified color mode index. |
| [`GET /monitors/{monitorId}/key-lock`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/getKeyLockSetting) | [get_key_lock_setting.py](./examples/key-lock/get_key_lock_setting.py) | Retrieves current key lock settings. |
| [`PUT /monitors/{monitorId}/key-lock`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/setKeyLockSetting) | [change_key_lock_setting.py](./examples/key-lock/change_key_lock_setting.py) | Changes the key lock setting with specified setting. |
| [`GET /monitors/{monitorId}/pixel-inspection`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/getPixelInspection) | [get_pixel_information.py](./examples/pixel-inspection/get_pixel_information.py) | Retrieves pixel information of specified coordinate. |
| [`PUT /monitors/{monitorId}/pixel-inspection/marker`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/setPixelInspectionMarker) | [change_marker_state.py](./examples/pixel-inspection/change_marker_state.py) | Changes the cross marker state of pixel inspection. |
| [`PUT /monitors/{monitorId}/selfcalibration/execution`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/setSelfCalibrationExecution) | [change_selfcalibration_execution_state.py](./examples/selfcalibration/change_selfcalibration_execution_state.py) | Changes the SelfCalibration execution state. |
| [`GET /monitors/{monitorId}/targets`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/getTargets) | [get_calibration_targets.py](./examples/targets/get_calibration_targets.py) | Retrieves information about all calibration targets. |
| [`POST /monitors/{monitorId}/targets`](https://www.eizoglobal.com/products/coloredge/developer/reference/cn-api.html#operation/createTarget) | [create_calibration_target.py](./examples/targets/create_calibration_target.py) | Creates a new calibration target. |

## Notes

- This example is intended to be used with Python 3.
- Example code is provided for reference. Ensure that you tailor the code to your specific use case and environment.
- Consult the ColorNavigator API documentation for detailed information on endpoints and parameters.

## License

This example code is provided under the MIT License. For more information, see the LICENSE file.
