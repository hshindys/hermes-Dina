' Hermes Agent Gateway - Messaging Platform Integration
Option Explicit
Dim sh, env, existing_pp
Set sh = CreateObject("WScript.Shell")
Set env = sh.Environment("PROCESS")
env.Item("HERMES_HOME") = "C:\Users\hshin\AppData\Local\hermes"
env.Item("PYTHONIOENCODING") = "utf-8"
env.Item("HERMES_GATEWAY_DETACHED") = "1"
env.Item("VIRTUAL_ENV") = "C:\Users\hshin\AppData\Local\hermes\hermes-agent\venv"
existing_pp = env.Item("PYTHONPATH")
If Len(existing_pp) > 0 Then
  env.Item("PYTHONPATH") = "C:\Users\hshin\AppData\Local\hermes\hermes-agent;" & existing_pp
Else
  env.Item("PYTHONPATH") = "C:\Users\hshin\AppData\Local\hermes\hermes-agent"
End If
sh.CurrentDirectory = "C:\Users\hshin\AppData\Local\hermes"
' Wait=True (last arg) so the task stays "running" for the gateway's lifetime;
' RestartOnFailure then restarts the GATEWAY process if it crashes on boot.
sh.Run "C:\Users\hshin\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m hermes_cli.main gateway run", 0, True
