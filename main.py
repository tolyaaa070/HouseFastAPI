from fastapi import FastAPI
import uvicorn
from house_app.api import property, review, auth, model_pkl
from house_app.api.auth import auth_router
import joblib
from pydantic import BaseModel

house_app = FastAPI()
house_app.include_router(property.property_router)
house_app.include_router(review.reviews_router)
house_app.include_router(auth.auth_router)
house_app.include_router(model_pkl.model_router)


if __name__ == '__main__':
    uvicorn.run(house_app , host='127.0.0.1' , port = 8000)


























