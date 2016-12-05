import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print message

jscode = """
Java.perform(function () {
	Java.enumerateLoadedClasses({
		onMatch: function(className) {
		    if(className != "Ljava/lang/Long;"){
				var clazz = Java.use(className);
				send(className);
			}
		},
		onComplete: function(){
			console.log("Done");
		}
	});
});
"""

process = frida.get_usb_device().attach('com.example.seccon2015.rock_paper_scissors')
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running CTF')
script.load()
sys.stdin.read()