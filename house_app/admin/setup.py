from .views import UserProfileAdmin,PropertyAdmin, ReviewsAdmin
from fastapi import FastAPI
from sqladmin import Admin
from house_app.db.database import engine

def setup_admin(house_app:FastAPI):
    admin = Admin(house_app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(PropertyAdmin)
    admin.add_view(ReviewsAdmin)
