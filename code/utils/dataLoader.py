import pandas as pd

class DataLoader:
    def __init__(self, file_path, piece_size):
        self.file_path = file_path
        self.piece_size = piece_size
        self.num_pieces = None
        
        self.df = pd.read_csv(file_path)
        self.num_pieces = int(len(self.df) / self.piece_size)
    
    def __len__(self):
        return self.num_pieces
    
    def __getitem__(self, index):
        if index >= self.num_pieces:
            raise IndexError("Index out of range")
        
        start_index = index * self.piece_size
        end_index = min((index + 1) * self.piece_size, len(self.df))
        
        piece_data_point = self.df.iloc[start_index:end_index]
        return piece_data_point