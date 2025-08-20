from house_app.db.model import UserProfile,Property,Reviews

from sqladmin import ModelView

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]

class PropertyAdmin(ModelView, model=Property):
    column_list = [Property.id , Property.title]


class ReviewsAdmin(ModelView , model = Reviews):
    column_list = [Reviews.property, Reviews.author ]