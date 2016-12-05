import sys

import frida


def main():
    argv = sys.argv
    process = None
    so_name = None
    func_name = None
    arg_count = len(argv)
    if arg_count < 2:
        print "this.py (pid|pName) [soName [funcName]]"
        return 1
    else:
        try:
            process = int(argv[1])
        except:
            process = argv[1]

    if arg_count > 2:
        so_name = argv[2]
    if arg_count > 3:
        func_name = argv[3]

    remote_dev = frida.get_remote_device()
    session = remote_dev.attach(process)
    modules = session.enumerate_modules()
    for module in modules:
        if so_name is None or so_name in module.name:
            print module
            export_funcs = module.enumerate_exports()
            for export_func in export_funcs:
                if func_name is None or func_name in export_func.name:
                    print "\t%s\t%s" % (export_func.name, hex(export_func.absolute_address))


if __name__ == "__main__":
    sys.exit(main())
