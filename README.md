# Keyboard + mouse switch

Press the **1** or **2** key on the MX Keys Mini (F1 / F2) and both the keyboard and the MX Master 3
move to that computer. No hardware: the same small script runs on both computers.

- Mac = channel 1, Windows = channel 2, on both the keyboard and the mouse.
- The keyboard's top row must send F-keys: press **Fn+Esc** once if F1 doesn't reach the computer.
  In that mode **Fn+F1 / Fn+F2** are still the keyboard's own Easy-Switch (keyboard only), as a backup.
- On the computer that has them, pressing the other computer's key sends the mouse there first,
  then the keyboard. It takes well under a second.

Why not the keyboard's own Easy-Switch? It switches inside the keyboard and tells the computer
nothing, so no script can make the mouse follow it. (Tested: `guided_test.py`.)

## Mac

```bash
git clone https://github.com/jenkasia/logitechmouseswitch.git && cd logitechmouseswitch
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # once
.venv/bin/python listener.py --channel 1 --dry-run   # press 2: prints what it would do, moves nothing
.venv/bin/python listener.py --channel 1             # for real
```

To start it at every login: `./setup_mac.sh` (remove with `./setup_mac.sh --uninstall`). The log is
`listener.log`. The first time, macOS blocks it from reading the keyboard: add the `Python.app` that the
log names in System Settings > Privacy & Security > Input Monitoring. It picks this up within a second.
After a Homebrew Python upgrade the path changes and you add it again.

## Windows

1. Install Python if it isn't there: `winget install Python.Python.3.12` (or python.org).
2. Get the files: `git clone https://github.com/jenkasia/logitechmouseswitch.git`, or on GitHub
   click **Code > Download ZIP** and unzip it somewhere simple, like `C:\Users\<you>\switch`.
3. Double-click `setup_windows.bat`. It installs hidapi, adds the switch to startup (no window) and
   starts it. The log is `listener.log` next to it.
4. Press **1** (F1) on Windows: the mouse and keyboard should come to the Mac.
   If nothing happens, press **Fn+Esc** once while on Windows and try again.

To run it by hand instead, with output in the console:

```bat
.venv\Scripts\python listener.py --channel 2 --dry-run
```

To remove it: `setup_windows.bat -Uninstall`.

On Windows the script takes F1 as a global hotkey, so F1 no longer reaches other programs there.
On the Mac, F2 also still reaches the app you're in.

## Files

- `listener.py`: the switch.
- `setup_mac.sh`, `setup_windows.bat` (+ `.ps1`): install it to start at login.
- `hidpp.py`: the small Logitech HID++ client it uses.
- `probe.py`, `guided_test.py`, `capture_keys.py`: read-only checks used while building it.

If the computer that has the devices is off or frozen, use Fn+F1 / Fn+F2 on the keyboard and the
Easy-Switch button under the mouse.
