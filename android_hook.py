import frida
import sys

if len(sys.argv) < 2:
    print "python android_hook.py (pid|pName) address"
    exit(0)

try:
    process = int(sys.argv[1])
except:
    process = sys.argv[1]

address = sys.argv[2]

remoteDev = frida.get_remote_device()
session = remoteDev.attach(process)

txt = """
Interceptor.attach(ptr("%s"), {
    onEnter: function(args) {
        send(Memory.readCString(args[3]));
        send("1: "+hexdump(Memory.readByteArray(args[1],4)));
        send("2: "+hexdump(Memory.readByteArray(args[2],4)));
        send("3: "+hexdump(Memory.readByteArray(args[3],4)));
        send("4: "+hexdump(Memory.readByteArray(args[4],4)));
        send("5: "+hexdump(Memory.readByteArray(args[5],4)));
    }
});
""" % int(address, 16)

script = session.create_script(txt)


def on_message(message, data):
    print "json ", message


script.on("message", on_message)
script.load()
sys.stdin.read()
