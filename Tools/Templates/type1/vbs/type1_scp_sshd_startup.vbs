WScript.Sleep 500
Set WshShell = WScript.CreateObject("WScript.Shell")
WScript.Sleep 1000
WshShell.Run "scp ""C:\Users\shaff\Desktop\Web Development\Django Websites\Tools\Templates\type1\linux\type1_sshd_config_startup"" root@255.255.255.255:/etc/ssh/sshd_config", 9
WScript.Sleep 3000

Msg2 = "yes"

For i = 1 To Len(Msg2)
   WScript.Sleep 1
   WshShell.SendKeys Mid(Msg2, i, 1)
Next

WshShell.SendKeys "{ENTER}"
WScript.Sleep 500

Msg3 = "p4ssw0rd"

For i = 1 To Len(Msg3)
   WScript.Sleep 1
   WshShell.SendKeys Mid(Msg3, i, 1)
Next

WshShell.SendKeys "{ENTER}"
WScript.Sleep 500