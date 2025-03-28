# Return

A simple tool to show a status marker in the system tray, based on the return code of a specifiable command.

## Blinky
```
return-monitor --interval 1 -- bash -ci '[ $RANDOM -gt 16384 ]'
```

## Autostart
Blinky example:
```
return-monitor --install --interval 1 -- bash -ci '[ $RANDOM -gt 16384 ]'
```

