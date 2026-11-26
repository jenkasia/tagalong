#!/bin/bash
# Installs the switch on this Mac and starts it at every login.
#   mac/setup.sh              asks for this computer's channel
#   mac/setup.sh 1            this computer is channel 1 (the Easy-Switch slot it's paired on)
#   mac/setup.sh --uninstall  stop it and remove it from login
set -euo pipefail
LABEL=local.keyboard-mouse-switch
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"
cd "$(dirname "$0")/.."
HERE="$PWD"   # the repo folder

stop_running() {
    launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null && echo "Stopped the running switch." || true
    for _ in 1 2 3 4 5 6 7 8 9 10; do   # launchd takes a moment to let go of it
        launchctl print "$DOMAIN/$LABEL" >/dev/null 2>&1 || return 0
        sleep 0.5
    done
}

if [ "${1:-}" = "--uninstall" ]; then
    stop_running
    rm -f "$PLIST" && echo "Removed it from login."
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

command -v python3 >/dev/null || { echo "Python 3 is not installed: brew install python (or python.org)"; exit 1; }
[ -x .venv/bin/python ] || python3 -m venv .venv
.venv/bin/pip install --quiet --disable-pip-version-check -r switch/requirements.txt
stop_running

mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>$HERE/.venv/bin/python</string>
        <string>$HERE/switch/listener.py</string>
        <string>--channel</string><string>$CHANNEL</string>
        <string>--log</string><string>$HERE/listener.log</string>
    </array>
    <key>WorkingDirectory</key><string>$HERE</string>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><dict><key>SuccessfulExit</key><false/></dict>
    <key>ProcessType</key><string>Interactive</string>
    <key>StandardErrorPath</key><string>$HERE/listener.err.log</string>
</dict>
</plist>
EOF
plutil -lint -s "$PLIST"
launchctl bootstrap "$DOMAIN" "$PLIST"
echo "Installed as channel $CHANNEL. It starts at every login: $PLIST"
sleep 3
echo
echo "Log ($HERE/listener.log):"
cat "$HERE/listener.log" 2>/dev/null || true
