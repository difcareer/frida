#coding = gbk

import frida
import sys
import json


def getFuncAddr(mds, lib, func):
    for m in mds:
        if lib == m.name:
            funcs = m.enumerate_exports()
            for f in funcs:
                if func == f.name:
                    return hex(f.absolute_address)
    return "0x0"


def on_message(message, data):
    if message["type"] == "send":
        print message["payload"], "\n--------------------------------------------------------------------------------\n"
    else:
        print message


txt = """
var address;
var flag = 0;
Interceptor.attach(ptr("$addr1"), {
    onEnter: function(args) {
        send(Memory.readCString(args[3]));
        flag = 1;
    },
    onLeave: function(retval){
        flag = 0;
    }
});

Interceptor.attach(ptr("$addr2"), {
    onEnter: function(args) {
        if(flag == 1){
            send(Memory.readCString(args[0]));
            flag = 0;
        }
    },
    onLeave: function(retval){

    }
});
"""

lib1 = "libutility.so"
func1 = "_ZN7YXImage12loadTextFileESs"

lib2 = "libc.so"
func2 = "strlen"

remoteDev = frida.get_remote_device()
session = remoteDev.attach("com.example.wechat01")
modules = session.enumerate_modules()

addr1 = getFuncAddr(modules, lib1, func1)
addr2 = getFuncAddr(modules, lib2, func2)

txt = txt.replace("$addr1", addr1)
txt = txt.replace("$addr2", addr2)

script = session.create_script(txt)
script.on("message", on_message)
script.load()
sys.stdin.read()
