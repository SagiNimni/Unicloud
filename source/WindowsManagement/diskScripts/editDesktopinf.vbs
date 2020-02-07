Set args = WScript.Arguments
EditDesktopIni args(0), args(1)

Sub EditDesktopIni(directory, iconpath)
	Dim fso, fold, inifile
	Const ForReading = 1, ForWriting = 2
	Const TristateUseDefault = -2, TristateTrue = -1, TristateFalse = 0
	Set fso = CreateObject("Scripting.FileSystemObject")
	Set fold = fso.GetFolder(directory)
	inifile = directory + "\desktop.ini"
	If (fso.FileExists(inifile)) Then
		fso.DeleteFile inifile, True
	End If 
	Set file = fso.OpenTextFile(inifile, ForWriting, True, TristateUseDefault)
	
	file.WriteLine "[.ShellClassInfo]"
	file.WriteLine "IconResource=" & iconpath & ",0"
	file.WriteLine "[ViewState]"
	file.WriteLine "Mode="
	file.WriteLine "Vid="
	file.WriteLine "FolderType=Generic"
End Sub	