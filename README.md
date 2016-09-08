# wakasha - A purely (self)entertainment software that listens for hotword and perfoms an action

## Configuration process
Copy and edit sample actio file:
```
cp wakasha/action/sample.py wakasha/action/action.py
```


## Build process
Go to https://snowboy.kitt.ai/, download or create model, store it within project directory
as model.pmdl
```make clean && make dmg```

## Installation and run
Click on DMG, drag icon to programs, open spotlight, type `wakasha`

NOTE: software will restart itself if killed or on system reboot


## Uninstall
```
launchctl unload ~/Library/LaunchAgents/com.example.wakasha.plist
ps ax|grep wakasha
```

if the app is still running, i.e. output is like this one:

```
2376   ??  S      0:00.05 /Applications/wakasha.app/Contents/MacOS/wakasha
2378 s003  S+     0:00.00 grep waka
```

run kill command with pid from the output (in this case):

```
kill 2376
```

then remove as any usual app
