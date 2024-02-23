import zipfile
import requests
import io
import requests
import os
import debug_utils as debug
import subprocess
import atexit
class DeamonService:

    deamon_path = '.\\deamon'
    application_path = deamon_path + "\\bin\\mtga-tracker-daemon.exe"
    deamon_process = None

    def open(self):
        self.download_mtga_tracker_deamon()
        self.run_application()
        print("teste")

    def download_mtga_tracker_deamon(self):
        
        if(self.is_downloaded()):
            return
        
        url = 'https://github.com/frcaton/mtga-tracker-daemon/releases/download/1.0.7.1/mtga-tracker-daemon-Windows.zip'
        response = requests.get(url)

        if response.status_code == 200:
            zip_content = io.BytesIO(response.content)

            with zipfile.ZipFile(zip_content, 'r') as zip_ref:
                zip_ref.extractall(deamon_path)
            
            print(f"Release downloaded and extracted to ")
        else:
            print(f"Failed to download release. Status code: {response.status_code}")


    def run_application(self):
        self.deamon_process
        if(self.deamon_process == None):
            return
        
        try:
            self.deamon_process = subprocess.Popen(self.application_path, shell=True)
            atexit.register(self.exit_handler, self.deamon_process)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


    def exit_handler(process):
        if process and process.poll() is None:
            print("Terminating the background process.")
            process.terminate()
            process.wait()

    def is_downloaded(self):
        return os.path.exists(self.deamon_path)

