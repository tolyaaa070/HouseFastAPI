from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import async_scoped_session

from house_app.db.model import Property
from house_app.db.schema import PropertyListSchema, PropertyCreateSchema
from house_app.db.database import SessionLocal
from typing import List
from sqlalchemy.orm import Session

property_router = APIRouter(prefix='/property' , tags=['Property'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@property_router.post('/', response_model=dict)
async def property_create(property : PropertyCreateSchema,
                         db: Session= Depends(get_db)):
    db_property = Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return {'message' : 'Успешно '}

@property_router.get('/',response_model=List[PropertyListSchema])
async def property_list(db: Session = Depends(get_db)):
    return db.query(Property).all()


@property_router.get('/{property_id}',response_model =PropertyListSchema)
async def property_detail(property_id: int, db: Session = Depends(get_db)):
    db_property = db.query(Property).filter(Property.id == property_id).first()

    if db_property is None:
        raise HTTPException(status_code=404, detail = 'Property Not Found')
    return db_property

@property_router.put('/{property_id}', response_model=dict)
async def property_update(property : PropertyCreateSchema,property_id: int,
                         db : Session = Depends(get_db)):
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail = 'Property Not Found')
    for property_key , property_value in property.dict().items():
        setattr(db_property , property_key,property_value)

        db.commit()
        db.refresh(db_property)

        return {'message':'Успешно!'}


@property_router.delete('/{property_id}/', response_model=dict)
async def property_delete(property_id: int, db: Session = Depends(get_db)):
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail = 'Property Not Found')
    db.delete(db_property)
    db.commit()
    return {'message': 'Удалено!'}


