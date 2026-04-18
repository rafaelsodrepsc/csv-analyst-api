import pandas as pd
from io import StringIO
import uuid
from fastapi import HTTPException
from services.executionService import safe_execute

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
def get_dataset(id):
    dataset = dictionary_zero.get(id)
    
    if dataset is None:
        raise HTTPException(status_code=404, detail="data set não encontrado")
        
    return {k: v for k,v in dataset.items() if k!="data"}

def preview_dataset(id: str, rows: int):
    dataset = dictionary_zero.get(id)
    
    if dataset is None:
        raise HTTPException(status_code=404, detail="data set não encontrado")
    
    df = dataset['data']
    
    return df.head(rows).to_dict(orient = 'records')

def execute_query(dataset_id: str, code: str) -> dict:
    dataset = dictionary_zero.get(dataset_id)

    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset não encontrado.")

    try:
        result = safe_execute(code, dataset["data"])
    except PermissionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TimeoutError as e:
        raise HTTPException(status_code=408, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na execução: {e}")

    # serializa o resultado independente do tipo
    if hasattr(result, "to_dict"):
        return {"result": result.to_dict(orient="records")}
    return {"result": str(result)}

from services import groqService, executionService

def query_dataset(id: str, pergunta: str) -> dict:
    dataset = dictionary_zero.get(id)

    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset não encontrado.")

    df = dataset["data"]

    colunas = list(df.columns)
    tipos = df.dtypes.astype(str).to_dict()
    amostra = df.head(3).to_dict(orient="records")

    codigo = groqService.gerar_codigo(pergunta, colunas, tipos, amostra)

    resultado = executionService.safe_execute(codigo, df)

    # Serializa o resultado independente do tipo
    if hasattr(resultado, "to_dict"):
        if hasattr(resultado, "columns"):
            resultado_final = resultado.to_dict(orient="records")
        else:
            resultado_final = resultado.to_dict()
    else:
        resultado_final = str(resultado)

    return {
        "pergunta": pergunta,
        "codigo_gerado": codigo,
        "resultado": resultado_final
    }
    