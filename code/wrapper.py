from model.Res1DTransformers_230220 import Res1D_Transformer_230220
from utils.dataLoader import DataLoader


data_path = 'data.csv'

loaded_data = DataLoader(data_path, piece_size=70)

Res1D_Transformer_230220.predict(loaded_data)