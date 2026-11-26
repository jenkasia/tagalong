# Troubleshooting

[← Back to the README](../README.md)

Look in `listener.log` in the repo folder first.

| Log says / what happens | Fix |
|---|---|
| `macOS won't let this program open it` | Add the `Python.app` it names under System Settings → Privacy & Security → Input Monitoring. |
| `this user may not open it` (Linux) | Run `linux/setup.sh` again: it adds the udev rule. Then unplug and reconnect the device, or reboot. |
| `waiting for the keyboard` and nothing else | The keyboard is on another computer, or not connected over Bluetooth. |
| `the top row is in special-function mode` | Press **Fn+Esc** once so the top row sends F-keys. |
| `could not take F1` (Windows) | Another program uses that key, often Logi Options+. Free it there and run the setup again. |
| `no mouse on this computer` | The mouse is already on another computer. Only the keyboard was sent. |
| `has only 2 channels, left it here` | That device has fewer channels than the one you pressed. |
| The key does nothing, no log line | The top row isn't sending F-keys (Fn+Esc), or the switch isn't running: run the setup again. |
| Stopped working after a Python upgrade (macOS) | The `Python.app` path changed: add the new one under Input Monitoring. |

## Try it by hand

`--dry-run` shows the key presses and what it would do, without moving anything.
Uninstall the background one first, so two don't run at once.

```bash
.venv/bin/python switch/listener.py --channel 1 --dry-run        # macOS / Linux
.venv\Scripts\python switch\listener.py --channel 2 --dry-run    # Windows
```

## If the computer with the devices is off or frozen

Use the keyboard's own Easy-Switch (**Fn+F1 / F2 / F3**) and the button under the mouse, as before.
