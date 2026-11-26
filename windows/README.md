# Windows

[← Back to the README](../README.md)

**Before you start:** the keyboard and the mouse are paired with this PC over Bluetooth, on the same channel
number, and **Fn+Esc** makes the top row send F-keys.

## Install

1. Install Python if it isn't there. In Terminal:

   ```bat
   winget install Python.Python.3.12
   ```

   Or get it from [python.org](https://www.python.org/downloads/windows/) with "py launcher" ticked.

2. Open the `windows` folder and double-click **`setup.bat`**.
   If Windows warns that the file came from the internet, click **More info → Run anyway**.
3. Type this PC's channel (1, 2 or 3). When it shows the log, close the window.

Done. It runs in the background with no window and starts at every sign-in.

## Test

Press another computer's F-key. The mouse and the keyboard should go there.

## Good to know

The other computers' F-keys become shortcuts for the switch, so they no longer reach other programs on this PC.

## Update / remove

| | |
|---|---|
| Update | Download the new ZIP over the same folder (or `git pull`), then double-click `setup.bat` again |
| Remove | In the `windows` folder, run `setup.bat -Uninstall` |

Something wrong? See [Troubleshooting](../docs/TROUBLESHOOTING.md).
