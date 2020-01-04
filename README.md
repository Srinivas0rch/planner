# Planner GNOME client

## About
Planner is a time management tool for linux desktops.
It combines the [Pomodoro technique](https://en.wikipedia.org/wiki/Pomodoro_Technique) and a simple Todo list.

It works by having clients connect to a time server via websockets.
This project represents a GNOME GUI **client**.
In order to work it needs to connect to [Planner time server](https://gitlab.com/i2002/planner-time-server).

## Screenshots
![Planner screenshot](https://gitlab.com/i2002/planner-gnome-client/raw/master/screenshots/planner.png)

## Installation
### Flatpak install
*TODO*

### Build
**Requirements**
- `python3`
- `websocket-client` python module
- GNOME environment
- `ninja`
- `meson`

1. Clone this repository
2. `cd <path-to-project>`
3. `meson . build`
4. `sudo ninja -C build install`

### Configure
To configure the ip and port for the time server connection, use `--ip` and `--port` command line arguments.

`planner --ip="127.0.0.1" --port="8888"`

## Licence
MIT
