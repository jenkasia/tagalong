"""Read-only check: list Logitech devices, their channels, and whether the Easy-Switch keys can be diverted.
Changes nothing on the devices."""
import hid

import hidpp

print("Logitech HID entries:")
for d in hid.enumerate(hidpp.LOGITECH, 0):
    print(f"  {d.get('product_string')!r} pid={d['product_id']:#06x} usage_page={d.get('usage_page', 0):#06x} usage={d.get('usage', 0):#06x}")

for info in hidpp.find_devices():
    print(f"\n== {info.product} (pid {info.pid:#06x})")
    try:
        dev = hidpp.Device(info)
    except OSError as e:
        print("  cannot open:", e)
        continue
    try:
        print("  name:", dev.name())
        n, cur = dev.host_info()
        print(f"  channels: {n}, current: {cur + 1}")
        for c in dev.controls():
            if c["cid"] in hidpp.HOST_SWITCH_CIDS:
                f = c["flags"]
                print(f"  key cid {c['cid']:#06x} (Easy-Switch {hidpp.HOST_SWITCH_CIDS[c['cid']] + 1}): flags={f:#04x}"
                      f" divertable={bool(f & hidpp.F_DIVERTABLE)} persist={bool(f & hidpp.F_PERSIST_DIVERTABLE)}")
    except hidpp.HidppError as e:
        print("  error:", e)
    finally:
        dev.close()
