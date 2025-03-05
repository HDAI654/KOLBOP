Set WshShell = CreateObject("WScript.Shell")

WshShell.Run "RS.vbs", 0, False

WshShell.Run "RC.vbs", 0, False
