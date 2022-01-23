import os
from time import time, sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

os.chdir('Path to directory')
last_change = time()

class Watchdog:
    global last_change
  
    def __init__(self):
        self.observer = Observer()
  
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, os.getcwd(), recursive = True)
        self.observer.start()

        try:
            while True:
                sleep(5)
                cooldown = time() - last_change
                if cooldown > 30 and cooldown < 35:
                    os.system('git push origin main')
        except:
            self.observer.stop()
            print('Watchdog stopped')
        self.observer.join()
  
  
class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        global last_change
        if '.git' in event.src_path or time() - last_change < 1.5:
            return

        path = event.src_path.split('/')
        subject = path[len(path) - 1]

        if event.event_type == 'created':
            os.system(f'git add {event.src_path}')
            os.system(f'git commit -a -m "Added {subject}"')
            last_change = time()

        elif event.event_type == 'modified':
            os.system(f'git commit -a -m "Updated {subject}"')
            last_change = time()

        elif event.event_type == 'deleted':
            os.system(f'git commit -a -m "Removed {subject}"')
            last_change = time()
  
watcher = Watchdog()
watcher.run()