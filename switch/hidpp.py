"""
Minimal HID++ 2.0 client for Logitech devices connected directly over Bluetooth.
(Devices behind a Bolt / Unifying USB receiver use device index 1..6; find_devices() doesn't list them yet.)

Only what the switch listener needs:
  - find a feature's index (root feature 0x0000)
  - CHANGE_HOST 0x1814: read the current channel, send the device to another channel
  - REPROG_CONTROLS_V4 0x1B04: list keys, divert keys to software
"""
from __future__ import annotations

import ctypes
import sys
import time
from dataclasses import dataclass

if sys.platform.startswith("linux"):
    # The default 'hid' module on Linux talks to USB through libusb and never sees Bluetooth devices.
    # The hidraw backend sees both.
    try:
        import hidraw as hid
    except ImportError:
        import hid
else:
    import hid

if sys.platform == "darwin":
    # hidapi opens devices exclusively on macOS by default, which fails for a keyboard and mouse
    # that macOS (and Logi Options+) already use. Open them shared instead.
    ctypes.CDLL(hid.__file__).hid_darwin_set_open_exclusive(0)

LOGITECH = 0x046D
HIDPP_PAGE = 0xFF43          # vendor usage page for HID++ over Bluetooth LE
HIDPP_PAGE_RECEIVER = 0xFF00  # Bolt / Unifying receiver
LONG = 0x11                  # long report: 20 bytes
LONG_LEN = 20
SW_ID = 0x0A                 # our software id, 1..15

ROOT = 0x0000
DEVICE_NAME = 0x0005
CHANGE_HOST = 0x1814
REPROG_V4 = 0x1B04

# Easy-Switch keys as REPROG_CONTROLS_V4 control ids
HOST_SWITCH_CIDS = {0x00D1: 0, 0x00D2: 1, 0x00D3: 2}   # cid -> channel index (0-based)

# 0x1B04 getCidInfo flags
F_DIVERTABLE = 0x20
F_PERSIST_DIVERTABLE = 0x40


_FEATURES: dict[tuple[int, int], int | None] = {}   # (product id, feature id) -> index; fixed per model


class HidppError(Exception):
    pass


@dataclass
class DeviceInfo:
    path: bytes
    product: str
    pid: int
    index: int        # HID++ device index: 0xFF for Bluetooth direct
    is_mouse: bool = False


def find_devices() -> list[DeviceInfo]:
    """Logitech devices that expose HID++ directly (Bluetooth). A device that also reports itself as a mouse
    (generic desktop page, usage 2) is marked is_mouse; that needs no request to the device."""
    entries = hid.enumerate(LOGITECH, 0)
    mice = {d["product_id"] for d in entries if d.get("usage_page") == 0x01 and d.get("usage") == 0x02}
    out, seen = [], set()
    for d in entries:
        if d.get("usage_page") == HIDPP_PAGE and d["path"] not in seen:
            seen.add(d["path"])
            out.append(DeviceInfo(d["path"], d.get("product_string") or "?", d["product_id"], 0xFF,
                                  d["product_id"] in mice))
    return out


class Device:
    def __init__(self, info: DeviceInfo):
        self.info = info
        self.h = hid.device()
        self.h.open_path(info.path)
        self.h.set_nonblocking(False)
        self.events: list[bytes] = []     # unsolicited reports read while waiting for a reply

    def close(self):
        try:
            self.h.close()
        except Exception:
            pass

    # ---- transport ----

    def _send(self, feat_idx: int, func: int, params: bytes = b"") -> None:
        msg = bytes([LONG, self.info.index, feat_idx, (func << 4) | SW_ID]) + params
        self.h.write(msg.ljust(LONG_LEN, b"\0"))

    def read(self, timeout_ms: int) -> bytes | None:
        r = self.h.read(64, timeout_ms)
        return bytes(r) if r else None

    def request(self, feat_idx: int, func: int, params: bytes = b"", timeout: float = 2.0) -> bytes:
        """Send a request and return the reply's parameter bytes (16 bytes)."""
        self._send(feat_idx, func, params)
        end = time.monotonic() + timeout
        while (left := end - time.monotonic()) > 0:
            r = self.read(max(1, int(left * 1000)))
            if not r or r[0] != LONG or r[1] != self.info.index:
                continue
            if r[2] == 0xFF and r[3] == feat_idx and r[4] == (func << 4) | SW_ID:
                raise HidppError(f"device error {r[5]:#x} for feature {feat_idx} function {func}")
            if r[2] == feat_idx and r[3] == (func << 4) | SW_ID:
                return r[4:]
            self.events.append(r)   # keep notifications that arrive in between
        raise HidppError("no reply from device")

    # ---- features ----

    def feature(self, feature_id: int) -> int | None:
        key = (self.info.pid, feature_id)
        if key not in _FEATURES:
            r = self.request(0, 0, feature_id.to_bytes(2, "big"))
            _FEATURES[key] = r[0] if (r[0] or feature_id == ROOT) else None
        return _FEATURES[key]

    def name(self) -> str:
        idx = self.feature(DEVICE_NAME)
        if not idx:
            return self.info.product
        n = self.request(idx, 0)[0]
        s = b""
        while len(s) < n:
            s += self.request(idx, 1, bytes([len(s)]))[: n - len(s)]
        return s.decode(errors="replace")

    def host_info(self) -> tuple[int, int]:
        """(number of channels, current channel 0-based)"""
        idx = self.feature(CHANGE_HOST)
        if not idx:
            raise HidppError("device has no CHANGE_HOST feature")
        r = self.request(idx, 0)
        return r[0], r[1]

    def change_host(self, channel: int) -> None:
        """Send the device to another channel (0-based). The device leaves at once and does not reply."""
        idx = self.feature(CHANGE_HOST)
        if not idx:
            raise HidppError("device has no CHANGE_HOST feature")
        self._send(idx, 1, bytes([channel]))

    def controls(self) -> list[dict]:
        idx = self.feature(REPROG_V4)
        if not idx:
            return []
        n = self.request(idx, 0)[0]
        out = []
        for i in range(n):
            r = self.request(idx, 1, bytes([i]))
            out.append(dict(cid=int.from_bytes(r[0:2], "big"), tid=int.from_bytes(r[2:4], "big"),
                            flags=r[4], pos=r[5], group=r[6], gmask=r[7], flags2=r[8]))
        return out

    def set_divert(self, cid: int, divert: bool) -> None:
        """Temporary divert: the key stops doing its own job and reports to software instead.
        The device forgets this when it reconnects or power-cycles."""
        idx = self.feature(REPROG_V4)
        # setCidReporting: cid, flags byte: bit0 divert, bit1 divert valid
        self.request(idx, 3, cid.to_bytes(2, "big") + bytes([0x02 | (0x01 if divert else 0)]))
