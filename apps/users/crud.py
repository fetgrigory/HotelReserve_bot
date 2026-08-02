from asgiref.sync import sync_to_async
from .models import User


# Adding the user to the database
@sync_to_async
def insert_user_data(telegram_id, first_name, last_name, phone):
    user = User.objects.filter(telegram_id=telegram_id).first()

    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.save()
    else:
        User.objects.create(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )


# Check if there is a user in the database
@sync_to_async
def check_user_exists(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).exists()
