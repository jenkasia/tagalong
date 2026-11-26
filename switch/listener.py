"""
Make a Logitech mouse (and any other Logitech device) follow your keyboard between computers.

Run this on every computer the devices are paired with, each with its own Easy-Switch channel:

  python switch/listener.py --channel 1     on the computer paired on channel 1
  python switch/listener.py --channel 2     on the computer paired on channel 2

The setup scripts in mac/, windows/ and linux/ install it to start at login.

Then press F1 / F2 / F3 for channel 1 / 2 / 3. The computer that has the devices right now sends every
Logitech device it has to that channel: mice first, then the keyboard. On many Logitech keyboards the
Easy-Switch keys are the F1-F3 keys, so you press the same key as before. The top row must send F-keys
(on MX keyboards, Fn+Esc toggles this); the keyboard's own Easy-Switch then stays on Fn+F1..F3.

--dry-run detects the key presses and says what it would do, without moving anything.
"""
from __future__ import annotations

import argparse
import signal
import sys
import time

import hidpp

FKEYS = {0x3A: 0, 0x3B: 1, 0x3C: 2}   # HID usage of F1, F2, F3 -> channel index (0-based)
POLL_S = 1.0
DEBOUNCE_S = 1.5

_log_file = None   # set by --log; started without a console (pythonw), print() goes nowhere


def log(*a):
    line = " ".join([time.strftime("%H:%M:%S"), *map(str, a)])
    if _log_file:
        _log_file.write(time.strftime("%Y-%m-%d ") + line + "\n")
        _log_file.flush()
    else:
        print(line, flush=True)


# ---------- switching ----------

def switch_all(target: int, dry_run: bool) -> None:
    """Send every HID++ device on this computer to channel `target` (0-based): others first, keyboard last."""
    devices = []
    for info in hidpp.find_devices():
        try:
            dev = hidpp.Device(info)
        except OSError as e:
            log(f"  cannot open {info.product}: {e}")
            continue
        try:
            if not dev.feature(hidpp.CHANGE_HOST):
                dev.close()
                continue
            n, cur = dev.host_info()
            devices.append((not info.is_mouse, dev, n, cur))
        except hidpp.HidppError as e:
            log(f"  {info.product}: {e}")
            dev.close()
    devices.sort(key=lambda t: t[0])          # mouse (False) before keyboard (True)
    if not any(not kb for kb, *_ in devices):
        log("  no mouse on this computer (it may be on the other one already)")
    for i, (is_kb, dev, n, cur) in enumerate(devices):
        name = dev.info.product
        try:
            if target >= n:
                log(f"  {name} has only {n} channels, left it here")
            elif cur == target:
                log(f"  {name} is already on channel {target + 1}")
            elif dry_run:
                log(f"  would send {name} to channel {target + 1}")
            else:
                if is_kb and i > 0:
                    time.sleep(0.15)          # let the mouse go first
                dev.change_host(target)
                log(f"  sent {name} to channel {target + 1}")
        finally:
            dev.close()


def warm_up() -> None:
    """Look up the feature numbers once now, so the first switch is as quick as the rest."""
    for info in hidpp.find_devices():
        try:
            dev = hidpp.Device(info)
            dev.feature(hidpp.CHANGE_HOST)
            dev.close()
        except (OSError, hidpp.HidppError):
            pass


class Trigger:
    def __init__(self, channel: int, dry_run: bool):
        self.channel, self.dry_run, self.last = channel, dry_run, 0.0

    def __call__(self, target: int) -> None:
        if target == self.channel - 1:
            log(f"key {target + 1}: already on this computer")
            return
        if time.monotonic() - self.last < DEBOUNCE_S:
            return
        self.last = time.monotonic()
        log(f"key {target + 1}: switching to channel {target + 1}")
        switch_all(target, self.dry_run)


# ---------- macOS (and other non-Windows systems): read the keyboard's own key reports ----------

_said_no_access = False


def find_keyboard() -> hidpp.Device | None:
    global _said_no_access
    for info in hidpp.find_devices():
        if info.is_mouse:
            continue
        try:
            return hidpp.Device(info)
        except OSError:
            if not _said_no_access:
                import os
                exe = os.path.realpath(sys.executable)
                if sys.platform == "darwin":
                    app = os.path.normpath(os.path.join(exe, "../../Resources/Python.app"))
                    log(f"{info.product} is connected, but macOS won't let this program open it. Add this app in "
                        f"System Settings > Privacy & Security > Input Monitoring, then it starts working by itself:\n"
                        f"    {app if os.path.isdir(app) else exe}")
                else:
                    log(f"{info.product} is connected, but this user may not open it ({info.path!r}). "
                        f"Give it read/write access to that device, for example with a udev rule.")
                _said_no_access = True
    return None


def warn_if_fn_lock_off(dev: hidpp.Device) -> None:
    """Feature 0x40A3 (fn inversion, MX Keys and similar). Byte 1 = 1 means the top row does special functions."""
    try:
        idx = dev.request(0, 0, (0x40A3).to_bytes(2, "big"))[0]
        if idx and dev.request(idx, 0)[1] == 1:
            log("NOTE: the top row is in special-function mode, so F1/F2 do the keyboard's own Easy-Switch and this "
                "script never sees them. Toggle fn lock (Fn+Esc on MX keyboards) so F1/F2 send F-keys.")
    except hidpp.HidppError:
        pass


def run_hid(trigger: Trigger) -> None:
    waiting_said = False
    while True:
        kb = find_keyboard()
        if not kb:
            if not waiting_said:
                log("waiting for the keyboard")
                waiting_said = True
            time.sleep(POLL_S)
            continue
        waiting_said = False
        log(f"{kb.info.product} is here, listening for F1/F2/F3")
        warn_if_fn_lock_off(kb)
        held: set[int] = set()
        try:
            while True:
                r = kb.events.pop(0) if kb.events else kb.read(int(POLL_S * 1000))
                if not r or r[0] != 0x01 or len(r) < 8:
                    continue
                now = set(r[2:8]) - {0}
                for key in now - held:
                    if key in FKEYS:
                        trigger(FKEYS[key])
                held = now
        except OSError:
            log("keyboard left")
        finally:
            kb.close()


# ---------- Windows: global hotkeys (Windows keeps keyboard reports to itself) ----------

def run_windows(trigger: Trigger) -> None:
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    MOD_NOREPEAT, WM_HOTKEY = 0x4000, 0x0312
    VK = {0: 0x70, 1: 0x71, 2: 0x72}          # VK_F1..VK_F3
    for ch, vk in VK.items():
        if ch != trigger.channel - 1:         # leave this computer's own key alone
            if not user32.RegisterHotKey(None, ch + 1, MOD_NOREPEAT, vk):
                log(f"could not take F{ch + 1} (another program uses it)")
    log("listening for " + ", ".join(f"F{ch + 1}" for ch in VK if ch != trigger.channel - 1))
    msg = wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
        if msg.message == WM_HOTKEY:
            trigger(msg.wParam - 1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--channel", type=int, required=True, choices=(1, 2, 3), help="this computer's channel")
    ap.add_argument("--dry-run", action="store_true", help="detect key presses, move nothing")
    ap.add_argument("--log", metavar="FILE", help="write the log to FILE (started over each run)")
    a = ap.parse_args()
    if a.log:
        global _log_file
        _log_file = open(a.log, "w", encoding="utf-8")
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    log(f"keyboard + mouse switch, this computer is channel {a.channel}{' (dry run)' if a.dry_run else ''}")
    trigger = Trigger(a.channel, a.dry_run)
    warm_up()
    if sys.platform == "win32":
        run_windows(trigger)
    else:
        run_hid(trigger)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("stopped")
    except Exception:
        import traceback
        log("crashed:\n" + traceback.format_exc())
        raise
