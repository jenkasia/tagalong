"""Turn on analytics key reporting for the Easy-Switch keys, log every HID++ report for a while, turn it off."""
import os
import sys
import time

import hid

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import hidpp  # noqa: E402

SECONDS = float(sys.argv[1]) if len(sys.argv) > 1 else 45


def kb_info():
    for info in hidpp.find_devices():
        if "Keys" in info.product:
            return info


def enable(dev, on):
    idx = dev.feature(hidpp.REPROG_V4)
    for cid in hidpp.HOST_SWITCH_CIDS:
        r = dev.request(idx, 3, cid.to_bytes(2, "big") + b"\x00" + b"\x00\x00" + bytes([0x02 | (1 if on else 0)]))
        print(f"  setCidReporting {cid:#06x} analytics={on}: reply {r[:6].hex()}", flush=True)


t0 = time.monotonic()
stamp = lambda: f"{time.monotonic() - t0:6.2f}s"
info = kb_info()
dev = hidpp.Device(info)
print(stamp(), "opened", info.product, "| features: reprog", dev.feature(hidpp.REPROG_V4), "change_host", dev.feature(hidpp.CHANGE_HOST), flush=True)
enable(dev, True)
print(stamp(), "PRESS KEYS NOW", flush=True)
end = t0 + SECONDS
while time.monotonic() < end:
    try:
        r = dev.read(500)
    except OSError as e:
        print(stamp(), "read error (keyboard gone?):", e, flush=True)
        dev.close()
        dev = None
        while time.monotonic() < end and dev is None:
            time.sleep(0.3)
            i = kb_info()
            if i:
                try:
                    dev = hidpp.Device(i)
                    print(stamp(), "keyboard back, reopened", flush=True)
                    enable(dev, True)
                except (OSError, hidpp.HidppError) as e2:
                    print(stamp(), "reopen failed:", e2, flush=True)
                    dev = None
        continue
    if r:
        print(stamp(), "report", r[:12].hex(" "), flush=True)
    elif not any(d["path"] == dev.info.path for d in hid.enumerate(hidpp.LOGITECH, 0)):
        print(stamp(), "keyboard no longer listed", flush=True)
if dev:
    try:
        enable(dev, False)
    except (OSError, hidpp.HidppError) as e:
        print("disable failed:", e)
    dev.close()
print(stamp(), "done", flush=True)
