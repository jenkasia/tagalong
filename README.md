# logitechmouseswitch

Press one key and your Logitech keyboard **and** mouse move to another computer together.

Logitech's Easy-Switch keys move only the keyboard: the mouse stays behind, and you have to reach under it
and press its own button. This tool fixes that with a small background script on each computer. It needs
no extra hardware, no cloud and no Logi Options+ Flow.

![How it works: you press F2, computer A hears it, sends the mouse and then the keyboard to channel 2, and both reach computer B](docs/how-it-works.svg)

## How it works

- Every computer the devices are paired with runs the script, set to that computer's Easy-Switch channel.
- You press **F1**, **F2** or **F3** to go to channel 1, 2 or 3.
- The computer that has the devices right now sends every Logitech device it has to that channel, mice first
  and then the keyboard. It uses the same command as the Easy-Switch buttons do (HID++ `CHANGE_HOST`).
- Only the computer that has the devices can send them away, which is why the script runs on all of them.

On many Logitech keyboards the Easy-Switch keys *are* F1–F3, so you keep pressing the same key as before.

## What you need

- Logitech devices with Easy-Switch, connected over **Bluetooth**. Devices on a Bolt or Unifying USB
  receiver aren't supported yet.
- Each computer paired on the **same channel number on every device**. For example, the computer on
  keyboard channel 1 is also on mouse channel 1.
- **Python 3.9 or newer** on each computer.
- **macOS** or **Windows**. Linux is untested; the macOS code path may work there with access to `/dev/hidraw*`.

Tested with an MX Keys Mini and an MX Master 3. Other Easy-Switch devices should work: `check.py` tells you.

## About Logitech Easy-Switch

Many Logitech keyboards and mice can be paired with up to **three computers** at once. Each pairing lives
in a numbered slot called a **channel** (1, 2, 3), and **Easy-Switch** is how you move between them:

- **Keyboards** have three Easy-Switch keys, often on F1–F3, marked with a computer icon and 1, 2, 3.
  A small light by the key shows the active channel.
- **Mice** have one Easy-Switch button underneath. Each press moves to the next channel, and three small
  lights show which one is active.

Each device switches on its own: pressing a keyboard's Easy-Switch key moves only the keyboard. That's the
gap this tool fills.

### Pair a device on a channel

This is the usual way for MX devices. Check your device's manual if it differs.

- **Keyboard:** hold the Easy-Switch key of the channel you want for about 3 seconds, until its light
  blinks fast. Then pair it from the computer's Bluetooth settings.
- **Mouse:** press the Easy-Switch button underneath until the light for the channel you want is on. Hold it
  for about 3 seconds, until the light blinks fast. Then pair it from the computer's Bluetooth settings.

Pairing a channel again replaces whatever was paired on it before.

### Which devices work

The tool needs devices that connect over Bluetooth and support the HID++ `CHANGE_HOST` feature. That's
the feature behind Easy-Switch, so in practice it means Logitech devices with Easy-Switch.

| Status | Devices |
|---|---|
| Tested | MX Keys Mini (Mac version), MX Master 3 |
| Likely to work, untested | Other MX keyboards and mice (MX Keys, MX Keys S, MX Mechanical, MX Master 3S, MX Anywhere 3), and other Easy-Switch devices such as the K380, K780 and Pebble series |
| Not yet | Any device connected through a Bolt or Unifying USB receiver |

To find out for sure, connect the device and run `check.py`. It says "can switch" for each device that works.
If you try one, an issue or pull request adding it to this table is welcome.

### Logi Options+

You don't need Logi Options+, and it can stay installed. Two things to watch:

- If Options+ gives the F1–F3 keys a custom action, the script may not get them. Set them back to the default.
- Options+ **Flow** does something similar (the mouse moves between computers at the screen edge), but it
  needs Options+ on every computer and all of them on the same network. This tool works without either.

## Setup

Do this on **every** computer the devices are paired with.

### 1. Pair the devices

Pair the keyboard and the mouse with the computer over Bluetooth, on a free Easy-Switch channel. Use the
same channel number on both devices. That number is this computer's channel.
See [Pair a device on a channel](#pair-a-device-on-a-channel) if you haven't done this before.

### 2. Get the files

```bash
git clone https://github.com/jenkasia/logitechmouseswitch.git
```

Or on GitHub click **Code → Download ZIP** and unzip it. Keep the folder somewhere permanent, since the
switch runs from it, and use a short path with no special characters.

### 3. Make the top row send F-keys

The script listens for F1–F3. If your keyboard's top row does media or Easy-Switch functions by default,
turn on fn lock so it sends F-keys. On MX keyboards, press **Fn+Esc** once.
The keyboard's own Easy-Switch then moves to **Fn+F1 / Fn+F2 / Fn+F3**.

### 4. Install

**macOS:** open Terminal in the folder and run:

```bash
./setup_macos.sh
```

**Windows:** double-click **`setup_windows.bat`**. If Windows warns that the file came from the internet,
click **More info → Run anyway**.

Both ask for this computer's channel (1, 2 or 3). Then they install what's needed, start the switch, and
set it to start at every login. It runs in the background with no window and writes `listener.log` in the folder.

If Python isn't installed, the setup says so:

- macOS: `brew install python`, or the installer from [python.org](https://www.python.org/downloads/).
- Windows: `winget install Python.Python.3.12`, or [python.org](https://www.python.org/downloads/windows/)
  with "py launcher" ticked.

**macOS only, the first time:** macOS doesn't let a background program read the keyboard until you allow
it. Open `listener.log`: it names a `Python.app`. Add that app in **System Settings → Privacy & Security →
Input Monitoring** and switch it on. The switch notices within a second, so you don't need to restart.

### 5. Test

When every computer is set up, press the F-key of another computer's channel. The mouse and the keyboard
should both move there within a second or two. Then press this computer's key on the other one to come back.

## Everyday use

| Press | Result |
|---|---|
| F1 / F2 / F3 | Keyboard and mouse go to channel 1 / 2 / 3 |
| The key of the computer you're on | Nothing, you're already there |
| Fn+F1 / Fn+F2 / Fn+F3 | The keyboard's own Easy-Switch: the keyboard only |

If the computer that has the devices is off or frozen, use Fn+F-key on the keyboard and the button under the
mouse, as before.

Side effects:

- **Windows:** the other channels' F-keys become global hotkeys, so they no longer reach other programs.
  This computer's own key stays free.
- **macOS:** the F-keys still reach the app you're in as well.

## Check your devices

`check.py` lists the Logitech devices connected right now, whether they can be switched, and which channel
they're on. It changes nothing. Run the setup first, or create `.venv` as shown.

macOS:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python check.py
```

Windows:

```bat
py -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python check.py
```

## Run it by hand

Useful for trying it out. `--dry-run` detects the keys and prints what it would do, without moving anything.
Uninstall the background one first, so two don't run at once.

```bash
.venv/bin/python listener.py --channel 1 --dry-run
```

On Windows use `.venv\Scripts\python` instead of `.venv/bin/python`.

## Troubleshooting

Look in `listener.log` first.

| Log says / what happens | Fix |
|---|---|
| `macOS won't let this program open it` | Add the named `Python.app` under Input Monitoring (step 4). |
| `waiting for the keyboard` and nothing else | The keyboard is on another computer, or not connected over Bluetooth. |
| `the top row is in special-function mode` | Turn on fn lock (step 3). |
| `could not take F1` (Windows) | Another program uses that key as a shortcut, often Logi Options+. Free the key there and run the setup again. |
| `no mouse on this computer` | The mouse is already on another computer. Only the keyboard was sent. |
| `has only 2 channels, left it here` | That device has fewer channels than the one you pressed. |
| Pressing the key does nothing, no log line | The top row isn't sending F-keys (step 3), or the switch isn't running: run the setup again. |
| It stopped working after a Python upgrade (macOS) | The `Python.app` path changed: add the new one under Input Monitoring. |

## Update

Get the new files (`git pull`, or download the ZIP again over the same folder), then run the setup again.

## Uninstall

macOS: `./setup_macos.sh --uninstall`. Windows: in the folder, run `setup_windows.bat -Uninstall`.

This stops the switch and removes it from login. Then you can delete the folder.

## Files

| File | What it is |
|---|---|
| `listener.py` | The switch |
| `hidpp.py` | A small Logitech HID++ 2.0 client (Bluetooth) |
| `check.py` | Lists your devices and their channels |
| `setup_macos.sh` | Installs it on macOS as a login item (LaunchAgent) |
| `setup_windows.bat`, `setup_windows.ps1` | Installs it on Windows in the Startup folder |
| `dev/` | Research scripts used to find out how the keyboard behaves |

## Why not watch the Easy-Switch key itself?

On the keyboards tested, the Easy-Switch keys can't be handed to software, and pressing one tells the computer
nothing before the keyboard leaves. So no program can see it in time to send the mouse along. Using the
F-key layer gets around that. `dev/guided_test.py` shows this for your own keyboard.

## Technical details

Logitech devices speak **HID++ 2.0**, a vendor protocol carried inside ordinary HID reports. Over Bluetooth
LE it uses a vendor HID collection (usage page `0xFF43`, usage `0x0202`) with 20-byte "long" reports
(report ID `0x11`, device index `0xFF`). Each request names a feature by its index, a function number and a
software ID. The device looks up the index for a feature ID through the root feature.

| Feature | ID | Used for |
|---|---|---|
| Root | `0x0000` | Finding the index of each feature below |
| Device name | `0x0005` | The device's name (in `check.py`) |
| Change host | `0x1814` | Function 0 reads the channel count and current channel. Function 1 sends the device to another channel: this is the switch. |
| Reprogrammable controls v4 | `0x1B04` | Reading the Easy-Switch keys' flags (in `check.py --verbose` and `dev/`) |
| Fn inversion | `0x40A3` | Warning when the top row isn't sending F-keys |

How each system gets the key press:

- **macOS:** the script reads the keyboard's own input reports (report ID `0x01`) through hidapi, opening the
  device in shared mode so macOS keeps using it too. That's why it needs Input Monitoring.
- **Windows:** Windows doesn't hand keyboard reports to other programs, so the script registers global hotkeys
  (`RegisterHotKey`) for the other channels' F-keys.

When the device receives `CHANGE_HOST` it disconnects right away without replying, so the script sends the
mouse first, then the keyboard.

[Solaar](https://github.com/pwr-Solaar/Solaar), a Linux manager for Logitech devices, is a good reference for
HID++.

## License

[MIT](LICENSE). Not affiliated with or endorsed by Logitech.
