import pandas as pd

class Data_Loading:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
    
    def load_data(self):
        """Reads the CSV file and stores it in the data attribute."""
        try:
            self.data = pd.read_csv(self.file_path)
            print(f"Data successfully loaded from {self.file_path}")
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
        except pd.errors.EmptyDataError:
            print(f"Error: No data in file {self.file_path}.")
        except pd.errors.ParserError:
            print(f"Error: Error parsing data in file {self.file_path}.")
    
    def get_data(self):
        """Returns the loaded data."""
        if self.data is not None:
            return self.data
        else:
            print("Data has not been loaded yet. Please call load_data first.")
            return None
