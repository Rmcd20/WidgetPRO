Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

projectDir = fso.GetParentFolderName(WScript.ScriptFullName)
pythonw = projectDir & "\.venv\Scripts\pythonw.exe"

If Not fso.FileExists(pythonw) Then
    MsgBox "Virtual environment not found. Run 'uv sync' in " & projectDir & " first.", 48, "WatchWidget"
    WScript.Quit 1
End If

shell.CurrentDirectory = projectDir
shell.Run """" & pythonw & """ -m watchwidget", 0, False
