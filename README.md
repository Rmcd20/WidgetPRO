WatchWidget
===========

Desktop world clock widget for Windows 11.

Run from PowerShell:

```powershell
uv sync
uv run python -m watchwidget
```

Start Without A Console Window
------------------------------

For Windows startup, use `start-watchwidget.vbs`. It launches the widget with
`.venv\Scripts\pythonw.exe`, so no empty Command Prompt window stays open.

Setup once:

```powershell
cd C:\Path\To\WidgetPRO
uv sync
```

Then add this file to startup:

```text
start-watchwidget.vbs
```

Quick startup-folder shortcut:

1. Press `Win + R`
2. Type `shell:startup`
3. Create a shortcut to `start-watchwidget.vbs`

Do not use `uv run` inside a startup `.bat` if you want zero console windows.
