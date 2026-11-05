@REM Windows counterpart of pixi-activate.sh: overlay the built colcon workspace.
@if exist "%PIXI_PROJECT_ROOT%\install\local_setup.bat" call "%PIXI_PROJECT_ROOT%\install\local_setup.bat"
@set "GZ_SIM_RESOURCE_PATH=%PIXI_PROJECT_ROOT%\.gazebo\models;%GZ_SIM_RESOURCE_PATH%"
