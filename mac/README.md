# macOS

[← Back to the README](../README.md)

**Before you start:** the keyboard and the mouse are paired with this Mac over Bluetooth, on the same channel
number, and **Fn+Esc** makes the top row send F-keys.

## Install

1. In Terminal, in the repo folder:

   ```bash
   mac/setup.sh
   ```

2. Type this Mac's channel (1, 2 or 3).
3. **First time only:** macOS blocks it from reading the keyboard. Open `listener.log`. It names a
   `Python.app`. Add that app in **System Settings → Privacy & Security → Input Monitoring** and turn it on.
   It starts working within a second.

Done. It runs in the background and starts at every login.

No Python? `brew install python`, or get it from [python.org](https://www.python.org/downloads/).

## Test

Press another computer's F-key. The mouse and the keyboard should go there.

## Update / remove

| | |
|---|---|
| Update | `git pull`, then `mac/setup.sh` again |
| Remove | `mac/setup.sh --uninstall` |

Something wrong? See [Troubleshooting](../docs/TROUBLESHOOTING.md).
