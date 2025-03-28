# Noti 

A simple tool to show a status marker in the system tray, based on the return code of a specifiable command.

## Install

```
pip install noti
```

## Blinky
```
noti --interval 1 -- bash -ci '[ $RANDOM -gt 16384 ]'
```

## Autostart
Blinky example:
```
noti --install --interval 1 -- bash -ci '[ $RANDOM -gt 16384 ]'
```

