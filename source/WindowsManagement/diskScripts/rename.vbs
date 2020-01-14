Set args = Wscript.Arguments
Set oShell = WScript.CreateObject("Shell.Application")
oShell.NameSpace(args(0) + "\").Self.Name = args(1)