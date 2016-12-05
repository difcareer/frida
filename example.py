import frida
session = frida.attach("sh.exe")
print([x.name for x in session.enumerate_modules()])