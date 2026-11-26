"""
Check which of your Logitech devices this tool can switch, and which channel each one is on now.
Read-only: it changes nothing on the devices.

  .venv/bin/python switch/check.py            (Windows: .venv\\Scripts\\python switch\\check.py)
  .venv/bin/python switch/check.py --verbose  also list every Logitech HID entry and the Easy-Switch key details
"""
import sys

import hidpp
from hidpp import hid   # the right HID backend for this system

verbose = "--verbose" in sys.argv

if verbose:
    print("Logitech HID entries:")
    for d in hid.enumerate(hidpp.LOGITECH, 0):
        print(f"  {d.get('product_string')!r} pid={d['product_id']:#06x} "
              f"usage_page={d.get('usage_page', 0):#06x} usage={d.get('usage', 0):#06x}")
    print()

devices = hidpp.find_devices()
if not devices:
    print("No Logitech Bluetooth devices found on this computer.")
    print("They need to be connected to this computer right now, over Bluetooth (not a USB receiver).")
    sys.exit(1)

ok = 0
for info in devices:
    kind = "mouse" if info.is_mouse else "keyboard or other"
    try:
        dev = hidpp.Device(info)
    except OSError as e:
        print(f"{info.product} ({kind}): cannot open it ({e}).")
        if sys.platform == "darwin":
            print("  On macOS, allow your terminal app in System Settings > Privacy & Security > Input Monitoring.")
        continue
    try:
        n, cur = dev.host_info()
        print(f"{info.product} ({kind}): can switch. {n} channels, on channel {cur + 1} now.")
        ok += 1
        if verbose:
            for c in dev.controls():
                if c["cid"] in hidpp.HOST_SWITCH_CIDS:
                    f = c["flags"]
                    print(f"  Easy-Switch key {hidpp.HOST_SWITCH_CIDS[c['cid']] + 1} (cid {c['cid']:#06x}): "
                          f"flags={f:#04x} divertable={bool(f & hidpp.F_DIVERTABLE)}")
    except hidpp.HidppError as e:
        print(f"{info.product} ({kind}): can't switch it ({e}).")
    finally:
        dev.close()

print()
if ok:
    print("The channel shown is this computer's channel: enter it when the setup asks.")
