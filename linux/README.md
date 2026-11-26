# Linux

[← Back to the README](../README.md)

> **Untested.** It uses the same code path as macOS, through hidraw. Reports welcome.

**Before you start:** the keyboard and the mouse are paired with this computer over Bluetooth, on the same
channel number, and **Fn+Esc** makes the top row send F-keys.

## Install

1. Install Python with venv support. For example, on Debian or Ubuntu:

   ```bash
   sudo apt install python3 python3-venv
   ```

2. In the repo folder:

   ```bash
   linux/setup.sh
   ```

3. Type this computer's channel (1, 2 or 3).
4. Enter your password when it asks for sudo. It adds a udev rule so you can open Logitech devices
   without root. This is a one-time step.

Done. It runs as a systemd user service and starts at every login.

## Test

Press another computer's F-key. The mouse and the keyboard should go there.

## Update / remove

| | |
|---|---|
| Update | `git pull`, then `linux/setup.sh` again |
| Remove | `linux/setup.sh --uninstall` (it tells you how to remove the udev rule too) |
| Status | `systemctl --user status logitech-switch` |

Something wrong? See [Troubleshooting](../docs/TROUBLESHOOTING.md).
