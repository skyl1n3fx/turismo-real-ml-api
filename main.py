"""

    API MACHINE LEARNING

"""

from fastapi import FastAPI, HTTPException, status
from joblib import load
from request.utils import find_dwelling, set_dwelling_data, generate_csv, dwelling_list, top_recommended
from fastapi.encoders import jsonable_encoder
from make_model import recommend

app = FastAPI()


# Server Definition
@app.get("/")
def root():
    return {"GoTo": "/docs"}

from fastapi.responses import JSONResponse

@app.get('/recommendations/{dwelling_id}')
async def search_recommendations(dwelling_id : int):
    if not dwelling_id:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=jsonable_encoder({'message' : 'Debe enviar un id.'})
            )
    # Verificamos si existe la vivienda
    if not find_dwelling(dwelling_id):
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=jsonable_encoder({'message' : 'No existe la vivienda.'})
            )
    # Generamos el csv y entrenamos el algoritmo
    #data = set_dwelling_data(dwelling_list(100).get('results'))
    #generate_csv('turismo_real',data)
    
    # hacemos la prediccion
    top = recommend(item_id = dwelling_id, num = 3)
    dwellings, message = top_recommended(top)
    print(dwellings)
    return {
        'message' : message.get('message'),
        'top' : dwellings
        }