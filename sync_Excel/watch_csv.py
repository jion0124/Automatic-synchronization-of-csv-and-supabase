import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ExcelFileHandler(FileSystemEventHandler):
    def __init__(self, file_path, script_path):
        self.file_path = file_path
        self.script_path = script_path

    def on_modified(self, event):
        if event.src_path.endswith(self.file_path):
            print(f"{self.file_path} has been modified. Running script...")
            python_executable = sys.executable  # Python実行ファイルのフルパスを取得
            subprocess.run([python_executable, self.script_path])

def monitor_excel_file(file_path, script_path, directory="."):
    event_handler = ExcelFileHandler(file_path, script_path)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    print(f"Monitoring changes to {file_path} in directory {directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    excel_file = "実験.csv"  # 監視するExcelファイルの名前
    python_script = "/Users/miyatajion/Downloads/明大祭実行委員会/sync_Excel/sync_to_supabase.py"  # 実行するPythonスクリプトのフルパス
    directory_to_watch = "/Users/miyatajion/Downloads/明大祭実行委員会/sync_Excel"  # 監視するディレクトリのフルパス

    monitor_excel_file(excel_file, python_script, directory_to_watch)
