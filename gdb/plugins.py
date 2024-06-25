import gdb

import argparse
import os
import shlex
import pathlib

class LocalParser(argparse.ArgumentParser):
    # Don't exit on error
    def error(self, message):
        self.print_help(sys.stderr)
        #self.exit(2, '%s: error: %s\n' % (self.prog, message))
        return None

class Plugins(gdb.Command):

    def __init__(self):
        super(Plugins, self).__init__("plugins", gdb.COMMAND_USER)
        this_dir = pathlib.Path(__file__).parent.resolve()
        self.plugin_dir = this_dir / "plugins"
        self.loaded = []
        
        parser = LocalParser()
        subparsers = parser.add_subparsers()
        list_parser = subparsers.add_parser("list", help="show plugins")
        list_parser.set_defaults(list=True, load=False)

        load_parser = subparsers.add_parser("load", help="load plugin")
        load_parser.add_argument("file")
        load_parser.set_defaults(list=False, load=True)

        self.parser = parser

    def list(self):
        for plugin_file in self.plugin_dir.iterdir():
            if plugin_file.is_file():
                name = plugin_file.name
                if name in self.loaded:
                    print("*",end="")
                else:
                    print(" ",end="")
                print(name)

    def load(self, file):
        pth = self.plugin_dir / file
        if pth.exists():
            gdb.execute(f"source {pth}")
            self.loaded.append(pth.name)
        else:
            print(f"{pth} does not exist")

    def invoke(self, arg, from_tty):
        args = shlex.split(arg)

        options = self.parser.parse_args(args)

        if not options:
            return

        if options.list:
            self.list()
        if options.load:
            self.load(options.file)
            
# Register the command with GDB
Plugins()

