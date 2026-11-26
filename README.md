<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <img src="docs/logo-light.svg" alt="Tagalong" width="380">
  </picture>
</p>

<p align="center"><b>Your mouse tags along when your Logitech keyboard switches computers.</b></p>

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
git clone https://github.com/jenkasia/logitechmouseswitch.git
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
