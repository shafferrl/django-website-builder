WScript.Sleep 500
Set WshShell = WScript.CreateObject("WScript.Shell")
WScript.Sleep 50
WshShell.Run "ssh -i C:\Users\shaff\.ssh\id_rsa root@255.255.255.255"
WScript.Sleep 1000



Msg2 = "chmod 700 type1_stack_script.sh"

For i = 1 To Len(Msg2)
   WScript.Sleep 1
   WshShell.SendKeys Mid(Msg2, i, 1)
Next

WshShell.SendKeys "{ENTER}"
WScript.Sleep 250



Msg3 = "source type1_stack_script.sh"

For i = 1 to Len(Msg3)
   WScript.Sleep 1
   WshShell.SendKeys Mid(Msg3, i, 1)
Next

WshShell.SendKeys "{ENTER}"
WScript.Sleep 500
