<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <img src="docs/logo-light.svg" alt="Tagalong" width="380">
  </picture>
</p>

<p align="center"><b>Your mouse tags along when your Logitech keyboard switches computers.</b></p>

<p align="center">
  <a href="https://github.com/jenkasia/tagalong/actions/workflows/ci.yml"><img src="https://github.com/jenkasia/tagalong/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="https://github.com/jenkasia/tagalong/actions/workflows/codeql.yml"><img src="https://github.com/jenkasia/tagalong/actions/workflows/codeql.yml/badge.svg?branch=main" alt="CodeQL security scan"></a>
  <a href=".github/dependabot.yml"><img src="https://img.shields.io/badge/dependabot-enabled-025E8C?logo=dependabot&logoColor=white" alt="Dependabot enabled"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/jenkasia/tagalong" alt="License: MIT"></a>
  <br>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+"></a>
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-555" alt="Platforms: macOS, Windows, Linux">
  <a href="switch/requirements.txt"><img src="https://img.shields.io/badge/dependencies-1%20%28hidapi%29-brightgreen" alt="Dependencies: 1 (hidapi)"></a>
  <a href="https://github.com/jenkasia/tagalong/commits/main"><img src="https://img.shields.io/github/last-commit/jenkasia/tagalong" alt="Last commit"></a>
  <a href="https://github.com/jenkasia/tagalong/stargazers"><img src="https://img.shields.io/github/stars/jenkasia/tagalong?style=flat" alt="GitHub stars"></a>
</p>

![Demo: press F2 and the mouse, then the keyboard, move from computer A to computer B](docs/demo.svg)

A small background script on each computer. No extra hardware, no cloud, no Logi Options+ Flow.

## Why

![Easy-Switch moves only the keyboard. Tagalong moves both.](docs/before-after.svg)

## How it works

![Press F2: computer A hears it and sends the mouse, then the keyboard, to channel 2](docs/how-it-works.svg)

- Press **F1 / F2 / F3** to go to channel **1 / 2 / 3**.
- The computer that has the devices sends them both there.

## What you need

- Logitech keyboard and mouse with **Easy-Switch**, connected over **Bluetooth** ([which devices](docs/LOGITECH.md#which-devices-work))
- Each computer on the **same channel number** on both devices

![Each computer has one channel number, the same on the keyboard and the mouse](docs/channels.svg)

## Setup

Do this on **every** computer:

![Setup: pair, download, F-keys on, run setup](docs/setup-steps.svg)

```bash
git clone https://github.com/jenkasia/tagalong.git
```

Or **Code → Download ZIP**. Then run the setup for your system:

| System | Setup | Guide |
|---|---|---|
| macOS | `mac/setup.sh` | [mac/](mac/README.md) |
| Windows | double-click `windows\setup.bat` | [windows/](windows/README.md) |
| Linux (untested) | `linux/setup.sh` | [linux/](linux/README.md) |

## Use

| Press | Result |
|---|---|
| F1 / F2 / F3 | Keyboard **and** mouse go to channel 1 / 2 / 3 |
| Fn+F1 / F2 / F3 | Keyboard only (Logitech's own Easy-Switch) |

## More

- [Logitech Easy-Switch, pairing and supported devices](docs/LOGITECH.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [How it works inside](docs/TECHNICAL.md)

## License

[MIT](LICENSE). Not affiliated with or endorsed by Logitech.
