# prevent_touchpad_toggle

![screenshot](screenshot.png)

Sets touch-pad on/off state repetitively in small intervals. Can be used in systems where touch-pad toggles itself or being toggled by accident.

- Tested on Ubuntu 20.04

- This app remembers the last toggle state between reboots. (Can be modified in `.py` file)
- Toggles touchpad on/off state every `0.25` seconds.

## Install

```bash
# Install dependencies
pip install PyQt5 python-is-python3

# Install the app
bash install.sh
```

- You can run `python3 $HOME/.local/share/prevent_touchpad_toggle_app/prevent_touchpad_toggle_app.py` or restart the computer. App will start in the system tray.

