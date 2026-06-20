from datetime import timedelta
from asgiref.sync import sync_to_async
from apps.bookings.models import Booking, ReservationDraft
from apps.users.models import User
from apps.rooms.models import Room


# Inserts a new booking record
@sync_to_async
def insert_booking_data(user_id, room_id, start_date, rent_days, total_price):
    end_date = start_date + timedelta(days=rent_days)

    user = User.objects.get(id=user_id)
    room = Room.objects.get(id=room_id)

    booking = Booking.objects.create(
        user=user,
        room=room,
        start_date=start_date,
        end_date=end_date,
        rent_days=rent_days,
        total_price=total_price
    )

    return booking


# Checking if the room is available
@sync_to_async
def is_room_available(room_id, start_date, end_date):
    return not Booking.objects.filter(
        room_id=room_id,
        start_date__lte=end_date,
        end_date__gte=start_date,
    ).exists()


# Retrieves the current reservation draft for a user
@sync_to_async
def get_user_reservation_draft(user_telegram_id: int):
    return ReservationDraft.objects.filter(
        user__user_id=user_telegram_id
    ).select_related(
        'apartment'
    ).prefetch_related(
        'services__service'
    ).first()


# Deletes a user's reservation draft
@sync_to_async
def delete_reservation_draft(user_telegram_id: int):
    ReservationDraft.objects.filter(user__user_id=user_telegram_id).delete()