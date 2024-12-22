import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file
        # Log dosyası yoksa otomatik olarak oluştur
        if not os.path.exists(log_file):
            os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Dizinleri oluştur
            with open(log_file, 'w') as f:
                f.write('')  # Boş dosya oluştur

    def on_modified(self, event):
        self.log_change(event)

    def on_created(self, event):
        self.log_change(event)

    def on_deleted(self, event):
        self.log_change(event)

    def log_change(self, event):
        change = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "is_directory": event.is_directory,
            "event_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"Logging change: {change}")
        with open(self.log_file, 'a') as f:
            json.dump(change, f, indent=4)
            f.write('\n')

if __name__ == "__main__":
    path_to_watch = "/home/mustafa/bsm/test"  # İzlenecek dizin
    log_file = "/home/mustafa/bsm/logs/changes.json"  # Log dosyası yolu

    event_handler = ChangeHandler(log_file)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    print(f"Watching for changes in: {path_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

