/**
 To use this with WinDbg first load the file

 (don't forgeta bout winpath)
 > .scriptload PATH_TO_FILE\HelloWindbg.js

 Then assign it to a variable.

 > dx @$hello = Debugger.State.Scripts.HelloWinDbg.Contents

 And invoke with

 > dx @$hello.sayHello("hi")
**/

// WinDbg JavaScript sample
function initializeScript()
{
    host.diagnostics.debugLog("Hello WinDbg! \n");
}

function sayHello(name) {
    let str = `Hello WinDbg, ${name}! \n`;
    host.diagnostics.debugLog(str);
    return str;
}
