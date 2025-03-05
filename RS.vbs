Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "venv\Scripts\python.exe NET_PRJ\manage.py runserver", 0, False