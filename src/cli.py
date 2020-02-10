#!/usr/bin/env python
# Copyright (C) 2019 Dan Makes

import sys
from app_manager import AppManager
import globals

Dandrop_app = None

class Cli():
    def __init__(self, args, options):
        self._args = args
        self._options = options

        self._usage = "usage: Dandrop start|stop|restart|create|status|config|factoryreset|help"

        self._app = AppManager(self.pid_file(), debug=self._options.debugmode)
        self._config = self._app._config
        self._globs = globals.Globals()

        self.parseArgs()

    def parseArgs(self):
        # Check for the correct numbers of arguments
        if len(self._args) < 1:
            self.print_help_message()
            sys.exit(2)

        if self._args[0] == 'start':
            self.start()
        elif self._args[0] == 'stop':
            self.stop()
        elif self._args[0] == 'restart':
            self.restart()
        elif self._args[0] == 'create':
            self.create()
        elif self._args[0] == 'status':
            self.status()
        elif self._args[0] == 'config':
            self.config()
        elif self._args[0] == 'factoryreset':
            pass
        elif self._args[0] == 'help':
            self.help()
        elif self._args[0] == 'rm':
            pass
        else:
            print "Unknown command"
            print self._usage
            sys.exit(2)

    def start(self):
        print "Starting DanDrop..."
        if self.stopped() and not self._options.debugmode:
            self._app.start()
        elif self.stopped() and self._options.debugmode:
            # Start in debug mode
            self._app.run()
        else:
            print "DanDrop is already running, please use restart"

    def stop(self):
        print "Stopping DanDrop..."
        if self.running:
            self._app.stop()
            print "DanDrop stopped"
        else:
            print "DanDrop is not running"

    def restart(self):
        self.stop()
        self.start()

    def create(self):
        if len(self._args) is not 5:
            print "False number of arguments!"
            return

        # Add new repository
        self._config.add_share(self._args[1], self._args[2], self._args[3], self._args[4])

        # Restart DanDrop
        if self.running(): self.restart()

    def status(self):
        print "DanDrop v" + self._globs.version
        print "Running: True" if self.running() else "Running: False"
        print "Shares:"
        print "\n".join("  - " + share.sync_folder for share in self._config.get_shares())

    def config(self):
        if len(self._args) == 1:
            # TODO: Print configuration
            print "Settings:"
            print "  - Log Level: " + self._config.logLevel
            print "  - API Listen IP: " + self._config.tcpListenIp
            print "  - API Listen Port: " + str(self._config.tcpListenPort)
            print "  - Web Server Enabled: " + str(self._config.enableWebServer)
            print "  - Web Server Listen IP: " + self._config.webServerListenIp
            print "  - Web Server Listen Port: " + str(self._config.webServerListenPort)
            print "  - Systray Enabled: " + str(self._config.enableSystray)
        elif len(self._args) > 1:
            pass

    def help(self):
        self.print_help_message()

    def running(self):
        return self._app.running()

    def stopped(self):
        return self._app.stopped()

    def pid_file(self):
        return "/tmp/Dandrop.pid"

    def print_help_message(self):
        print self._usage
        print "Type Dandrop -h or Dandrop --help to get more information about all options"
        print
        print "Commands:"
        print "  start          Start DanDrop"
        print "  stop           Stop DanDrop"
        print "  restart        Restart DanDrop"
        print "  create         Create and add a new share."
        print "                 Usage: create sync_directory remote_host remote_directory remote_user"
        print "  rm             Removes the specified share"
        print "  status         Shows the current status"
        print "  config         Shows the current configuration"
        print "  factoryreset   Resets all settings"
        print "  help           Prints this help message"
