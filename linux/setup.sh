#!/bin/bash
# Installs the switch on this Linux computer and starts it at every login (systemd user service).
#   linux/setup.sh              asks for this computer's channel
#   linux/setup.sh 3            this computer is channel 3 (the Easy-Switch slot it's paired on)
#   linux/setup.sh --uninstall  stop it and remove it from login
set -euo pipefail
UNIT=logitech-switch.service
UNIT_FILE="$HOME/.config/systemd/user/$UNIT"
RULE=/etc/udev/rules.d/70-logitech-switch.rules
cd "$(dirname "$0")/.."
HERE="$PWD"   # the repo folder

if [ "${1:-}" = "--uninstall" ]; then
    systemctl --user disable --now "$UNIT" 2>/dev/null || true
    rm -f "$UNIT_FILE"
    systemctl --user daemon-reload
    echo "Removed it from login."
    [ -f "$RULE" ] && echo "The device access rule stays in $RULE. To remove it: sudo rm $RULE"
    exit 0
fi

CHANNEL="${1:-}"
if [ -z "$CHANNEL" ]; then
    read -r -p "Which Easy-Switch channel is this computer on (1, 2 or 3)? " CHANNEL
fi
case "$CHANNEL" in
    1|2|3) ;;
    *) echo "The channel must be 1, 2 or 3."; exit 1 ;;
esac

command -v python3 >/dev/null || { echo "Python 3 is not installed. Install python3 and python3-venv."; exit 1; }
[ -x .venv/bin/python ] || python3 -m venv .venv || { echo "Install python3-venv (Debian/Ubuntu: sudo apt install python3-venv)."; exit 1; }
.venv/bin/pip install --quiet --disable-pip-version-check -r switch/requirements.txt

# Let the logged-in user open Logitech HID devices (USB and Bluetooth), the same way Solaar does.
if [ ! -f "$RULE" ]; then
    echo "Adding a udev rule so you can open Logitech devices (needs sudo):"
    sudo tee "$RULE" >/dev/null <<'EOF'
# logitechmouseswitch: let the logged-in user open Logitech HID devices
ACTION!="add|change", GOTO="logitech_switch_end"
SUBSYSTEM!="hidraw", GOTO="logitech_switch_end"
ATTRS{idVendor}=="046d", TAG+="uaccess", GOTO="logitech_switch_end"
KERNELS=="0005:046D:*", TAG+="uaccess"
LABEL="logitech_switch_end"
EOF
    sudo udevadm control --reload-rules
    sudo udevadm trigger --subsystem-match=hidraw
fi

mkdir -p "$(dirname "$UNIT_FILE")"
cat > "$UNIT_FILE" <<EOF
[Unit]
Description=Logitech keyboard + mouse switch (channel $CHANNEL)

[Service]
ExecStart="$HERE/.venv/bin/python" "$HERE/switch/listener.py" --channel $CHANNEL --log "$HERE/listener.log"
WorkingDirectory=$HERE
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --quiet "$UNIT"
systemctl --user restart "$UNIT"
echo "Installed as channel $CHANNEL. It starts at every login: $UNIT_FILE"
sleep 3
echo
echo "Log ($HERE/listener.log):"
cat "$HERE/listener.log" 2>/dev/null || true
