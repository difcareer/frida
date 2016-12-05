import sys

import frida


def main():
    remote_dev = frida.get_remote_device()
    session = remote_dev.attach("com.example.wechat01")
    modules = session.enumerate_modules()
    for module in modules:
        print module
        export_funcs = module.enumerate_exports()
        for export_func in export_funcs:
            if "strlen" == export_func.name:
                print "\t%s\t%s" % (export_func.name, hex(export_func.absolute_address))

if __name__ == "__main__":
    sys.exit(main())
