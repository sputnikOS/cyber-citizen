import os
import Pyro4

class NAS_Server:
    def __init__(self, storage_directory):
        self.storage_directory = storage_directory

    def list_files(self):
        return os.listdir(self.storage_directory)

    def upload_file(self, file_data, file_name):
        with open(os.path.join(self.storage_directory, file_name), 'wb') as file:
            file.write(file_data)
        return True

    def download_file(self, file_name):
        file_path = os.path.join(self.storage_directory, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                return file.read()
        else:
            return None

if __name__ == '__main__':
    storage_directory = ''  # Replace with your storage directory
    nas_server = NAS_Server(storage_directory)

    with Pyro4.Daemon() as daemon:
        uri = daemon.register(nas_server)
        print("NAS Server URI:", uri)

        with Pyro4.locateNS() as ns:
            ns.register("nas_server", uri)

        print("NAS Server is ready.")
        daemon.requestLoop()
