"""
Guided Easy-Switch test. Tells you which key to press, records what the keyboard sends for each step,
and prints a summary. Changes nothing permanent: key reporting is turned off again at the end.

  .venv/bin/python guided_test.py
"""
import time

import hid

import hidpp

STEP_S = 5.0
COME_BACK_S = 20.0
KEYS = {0x3A: "F1", 0x3B: "F2", 0x3C: "F3", 0x29: "Esc"}
STEPS = ["F1", "F2", "Fn+F1", "Fn+F2"]


def kb_info():
    for info in hidpp.find_devices():
        if "Keys" in info.product:
            return info


def set_analytics(dev, on):
    idx = dev.feature(hidpp.REPROG_V4)
    for cid in hidpp.HOST_SWITCH_CIDS:
        dev.request(idx, 3, cid.to_bytes(2, "big") + b"\x00\x00\x00" + bytes([0x02 | (1 if on else 0)]))


def open_kb():
    info = kb_info()
    if not info:
        return None
    dev = hidpp.Device(info)
    set_analytics(dev, True)
    return dev


def describe(r: bytes) -> str | None:
    if r[0] == 0x01:                      # ordinary keyboard report: modifiers, reserved, 6 keys
        keys = [KEYS.get(k, f"key {k:#04x}") for k in r[2:8] if k]
        return ("press " + "+".join(keys)) if keys else None
    if r[0] == hidpp.LONG:
        return "HID++ " + r[:10].hex(" ")
    return "report " + r[:10].hex(" ")


def watch(dev, seconds):
    """Collect what happens for `seconds`. Returns (events, dev) - dev is None if the keyboard left."""
    events, end = [], time.monotonic() + seconds
    while time.monotonic() < end:
        try:
            r = dev.read(200)
        except OSError:
            events.append("keyboard DISCONNECTED")
            dev.close()
            return events, None
        if r:
            d = describe(bytes(r))
            if d:
                events.append(d)
        elif not any(x["path"] == dev.info.path for x in hid.enumerate(hidpp.LOGITECH, 0)):
            events.append("keyboard DISCONNECTED")
            dev.close()
            return events, None
    return events, dev


def main():
    dev = open_kb()
    if not dev:
        print("Keyboard not found.")
        return
    results = []
    try:
        print("Don't type anything else during the test.\n")
        time.sleep(1.5)
        for step in STEPS:
            print(f">>> Press {step} once now", flush=True)
            events, dev = watch(dev, STEP_S)
            results.append((step, events))
            print("    " + ("; ".join(events) or "nothing"), flush=True)
            if dev is None:
                print(f">>> The keyboard left. Press Fn+F1 to bring it back (waiting up to {COME_BACK_S:.0f} s)", flush=True)
                end = time.monotonic() + COME_BACK_S
                while dev is None and time.monotonic() < end:
                    time.sleep(0.3)
                    try:
                        dev = open_kb()
                    except (OSError, hidpp.HidppError):
                        dev = None
                print("    keyboard is back" if dev else "    keyboard did not come back, stopping", flush=True)
                if dev is None:
                    break
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        if dev:
            try:
                set_analytics(dev, False)
            except (OSError, hidpp.HidppError):
                pass
            dev.close()

    print("\nSummary")
    for step, events in results:
        print(f"  {step:6} -> {'; '.join(events) or 'nothing'}")


if __name__ == "__main__":
    main()
