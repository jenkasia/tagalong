# Windows setup

Once this is set up, pressing **1** (the F1 key) on the keyboard while you're on Windows sends both the
keyboard and the mouse to the Mac. The Mac side sends them here when you press **2** there.

## Before you start

- The keyboard and the mouse are paired with this PC over Bluetooth on **channel 2**: the keyboard's
  Easy-Switch key 2 and channel 2 on the button under the mouse. If they already work on this PC, you're done.
- Python is installed. To check, open **Terminal** (or Command Prompt) and type `py --version`.
  If it says the command isn't found, install it:

  ```bat
  winget install Python.Python.3.12
  ```

  Or download it from [python.org](https://www.python.org/downloads/windows/) and keep
  "py launcher" ticked during setup. Close and reopen the terminal afterwards.

## Install

1. On the [repo page](https://github.com/jenkasia/logitechmouseswitch), click **Code → Download ZIP**.
2. Unzip it into a short path with no special characters, for example `C:\Users\<you>\switch`.
   Leave it there: the switch runs from that folder.
3. Open the folder and double-click **`setup_windows.bat`**.
   - If Windows warns that the file came from the internet, click **More info → Run anyway**.
   - A window opens. It installs what's needed, adds the switch to startup and starts it.
     When it shows the log and "Press any key", close it.

The switch now runs in the background with no window, and it starts again every time you sign in.

## Test it

Press **1** on the keyboard. The mouse and the keyboard should both move to the Mac within a second or two.

If nothing happens:

1. Press **Fn+Esc** once, then press **1** again. This toggles the top row between F-keys and
   the keyboard's own functions, and the switch needs F-keys.
2. Open `listener.log` in the folder. It should say `listening for F1, F3`.
   - `could not take F1`: another program uses F1 as a shortcut. Logi Options+ is the usual one;
     set F1 back to its default there, then run `setup_windows.bat` again.
   - Something else: send the log to whoever set this up.

## Good to know

- Press **1** to go to the Mac. Pressing **2** on Windows does nothing, because you're already here.
- On this PC, F1 now belongs to the switch and no longer reaches other programs.
- **Fn + the 1 key** still switches only the keyboard, using its own Easy-Switch. If the switch isn't running,
  use that, plus the button under the mouse.

## Update or remove

- **Update:** download the ZIP again, unzip it over the same folder and double-click `setup_windows.bat`.
- **Remove:** in that folder, open a terminal and run `setup_windows.bat -Uninstall`. It stops the switch
  and takes it out of startup. Then you can delete the folder.
