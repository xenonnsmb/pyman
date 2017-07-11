#!/usr/bin/env python
# Pyman (1.1) by XenonNSMB
# MIT licensed.

# To configure Pyman, skip to line 14.
from time import sleep
import subprocess
import atexit
import web
global tasks
global correct
tasks = {}
web.config.debug = False
def Config():
    # This is Pyman's config section. Edit it to change how Pyman works.

    # To add tasks, use syntax like this:
    # t = main.Task() # Create a new Task class.
    # t.path = "/path/to/your/script.py" # Path to your task's script.
    # t.filename = "script.py" # Filename, for use in pkill when killing your task.
    # t.name = "Example task" # Display name for your task.
    # t.startup = False # Whether or not to run the script when Pyman starts up. Defaults to True
    # t.pythonver = "python3" # Which program to call when running your script. Defaults to python3.
    # main.RegTask(t) # Register your task.
class Task():
    def __init__(self):
        self.name = "undefined"
        self.path = "undefined"
        self.pythonver = "python3"
        self.startup = True
        self.filename = "undefined"
        self.running = False
    def start(self):
        subprocess.Popen([self.pythonver, self.path], stdout=subprocess.PIPE)
        self.running = True
        print("Started task " + self.name)
    def kill(self):
        subprocess.Popen(["pkill", "-f", self.filename])
        print("Killed task " + self.name)
        self.running = False
def RegTask(Task):
    n = Task.name
    tasks[n] = Task
    print("Registered task " + n)
    if (Task.startup == True):
        Task.start()
def ProperExit():
    print("Killing tasks...")
    global tasks
    for t in tasks:
        tasks[t].kill()
    print("Finished killing tasks.")
    print("Thanks for using Pyman.")
atexit.register(ProperExit)
urls = ('/', 'manager')
render = web.template.render('templates/')
app = web.application(urls, globals())
class manager:
    def GET(self):
        global tasks
        msg = "Welcome to pyman. " + str(len(tasks)) + " tasks registered:"
        for t in tasks:
            msg = msg + "<br>" + t
            if (tasks[t].running == True):
                msg = msg + " - running"
            msg = msg + " <button onclick=\"starttask(\'" + t + "\')\">Start</button>" + " <button onclick=\"stoptask(\'" + t + "\')\">Stop</button>"
        return render.manager(msg)
    def POST(self):
        thingtostart = web.input().task
        thetype = web.input().type
        global tasks
        if (thetype == "start"):
            tasks[thingtostart].start()
            return render.manager("Starting task " + thingtostart + "...")
        else:
            tasks[thingtostart].kill()
            return render.manager("Stopping task " + thingtostart + "...")
if __name__ == "__main__":
    Config()
    app.run()
    print("Server finished")
    exit()
