#!/bin/bash
# Sets up the keyboard + mouse switch on the Mac (channel 1) and starts it at every login.
#   ./setup_mac.sh              install (again) and start
#   ./setup_mac.sh --uninstall  stop it and remove it from login
set -euo pipefail
CHANNEL=1
LABEL=local.keyboard-mouse-switch
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"
cd "$(dirname "$0")"
HERE="$PWD"

launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null && echo "Stopped the running switch." || true

if [ "${1:-}" = "--uninstall" ]; then
    rm -f "$PLIST" && echo "Removed it from login."
    exit 0
fi

[ -x .venv/bin/python ] || python3 -m venv .venv
.venv/bin/pip install --quiet --disable-pip-version-check -r requirements.txt

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
        <string>$HERE/listener.py</string>
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
echo "Added to login: $PLIST"
sleep 3
echo
echo "Log ($HERE/listener.log):"
cat "$HERE/listener.log" 2>/dev/null || true
