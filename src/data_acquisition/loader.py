import os
try:
    from roboflow import Roboflow
except ImportError:
    Roboflow = None

class DatasetLoader:
    def __init__(self, api_key, workspace, project, version_num=1):
        self.api_key = api_key
        self.workspace = workspace
        self.project = project
        self.version_num = version_num

    def download_data(self, download_path="data/raw"):
        if Roboflow is None:
            print("[Eroare] Biblioteca roboflow nu este instalată.")
            return None
            
        print(f"[DataAcquisition] Descărcare în {download_path}...")
        try:
            rf = Roboflow(api_key=self.api_key)
            project = rf.workspace(self.workspace).project(self.project)
            version = project.version(self.version_num)
            
            # Schimbăm directorul temporar pentru descărcare
            original_cwd = os.getcwd()
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            os.chdir(download_path)
            
            dataset = version.download("yolov11")
            os.chdir(original_cwd)
            return dataset
        except Exception as e:
            print(f"[Eroare] {e}")
            return None
