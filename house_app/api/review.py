from fastapi import Depends, HTTPException, APIRouter
from house_app.db.model import Reviews
from house_app.db.schema import ReviewsSchema, ReviewsCreateSchema
from house_app.db.database import SessionLocal
from typing import List
from sqlalchemy.orm import Session


reviews_router = APIRouter(prefix='/reviews', tags=['Reviews'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@reviews_router.post('/', response_model=dict)
async def reviews_create(review: ReviewsCreateSchema,
                         db: Session= Depends(get_db)):
    db_review = Reviews(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return {'message' : 'Успешно'}


@reviews_router.get('/',response_model=List[ReviewsSchema])
async def reviews_list(db: Session = Depends(get_db)):
    return db.query(Reviews).all()

@reviews_router.get('/{reviews_id}',response_model=ReviewsSchema)
async def reviews_detail(reviews_id :int, db: Session = Depends(get_db)):
    db_reviews = db.query(Reviews).filter(Reviews.id == reviews_id).first()
    if db_reviews is None:
        raise HTTPException(status_code=404 , detail='Not Found')
    return db_reviews


@reviews_router.put('/{reviews_id}',response_model=dict)
async def reviews_update(reviews : ReviewsCreateSchema,reviews_id : int,
                         db: Session = Depends(get_db)):
    db_reviews = db.query(Reviews).filter(Reviews.id == reviews_id).first()
    if not db_reviews:
        raise HTTPException(status_code=404, detail = 'Not Found')
    for reviews_key , reviews_value in reviews.dict().items():
        setattr(db_reviews,reviews_key, reviews_value)

        db.commit()
        db.refresh(db_reviews)

    return {'message' : 'Успешно!'}


@reviews_router.delete('/{reviews_id}',response_model=dict)
async def reviews_delete(reviews_id :int, db: Session = Depends(get_db)):
    db_reviews = db.query(Reviews).filter(Reviews.id == reviews_id).first()
    if db_reviews is None:
        raise HTTPException(status_code=404 , detail='Not Found')

    db.delete(db_reviews)
    db.commit()
    return {'message':'Успешно!'}
