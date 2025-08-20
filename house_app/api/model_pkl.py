from fastapi import FastAPI, APIRouter
import joblib
from pydantic import BaseModel


model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
model_router = APIRouter(prefix='/model_pkl' , tags=['Model_pkl'])
nei = ['Blueste', 'BrDale', 'BrkSide', 'ClearCr',
       'CollgCr', 'Crawfor', 'Edwards', 'Gilbert',
       'IDOTRR', 'MeadowV', 'Mitchel', 'NAmes',
       'NPkVill', 'NWAmes', 'NoRidge', 'NridgHt',
       'OldTown', 'SWISU', 'Sawyer', 'SawyerW',
       'Somerst', 'StoneBr', 'Timber', 'Veenker']
class House(BaseModel):
        GrLivArea: int
        YearBuilt :int
        GarageCars: int
        TotalBsmtSF: int
        FullBath : int
        OverallQual : int
        Neighborhood: str

@model_router.post('/predict')
async def check_score(house :House):
    db_house = house.dict()

    new_neighborhood = db_house.pop('Neighborhood')
    neighborhood1_0 = [
        1 if new_neighborhood == i else 0 for i in nei
    ]

    features = list(db_house.values()) + neighborhood1_0
    scaled = scaler.transform([features])
    pred = model.predict(scaled)[0]
    return {'Примерный price' : round(pred, 2) }






























