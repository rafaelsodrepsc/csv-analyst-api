import pandas as pd
from io import StringIO
import uuid

dictionary_zero = {}

def process_upload(filename: str, content: bytes) -> dict:
    try:
        strContent = content.decode('utf-8')
    except UnicodeDecodeError:
        strContent = content.decode('latin-1')
    csvFile = StringIO(strContent)

    reader = pd.read_csv(csvFile, sep= None, engine= 'python')
    
    uuid_object = str(uuid.uuid4())
    
    dictionary_zero[uuid_object] =  {
        "id": uuid_object,
        "nome": filename,
        "colunas": list(reader.columns),
        "shape": reader.shape,
        "data": reader  
    }
    
    return {
        "id": uuid_object,
        "nome": filename,
        "colunas": list(reader.columns),
        "shape": reader.shape,
    }

def list_datasets():
    return [
        {k: v for k, v in dataset.items() if k != "data"}
        for dataset in dictionary_zero.values()
        ]