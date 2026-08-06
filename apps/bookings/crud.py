from datetime import timedelta

from asgiref.sync import sync_to_async

from apps.bookings.models import Booking, ReservationDraft
from apps.users.models import User
from apps.rooms.models import Room


# Inserts a new booking record
@sync_to_async
def insert_booking_data(
    telegram_id,
    room_id,
    start_date,
    rent_days,
    total_price
):
    end_date = start_date + timedelta(days=rent_days)

    user = User.objects.get(telegram_id=telegram_id)
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


# Adds room to user's reservation draft
@sync_to_async
def add_room_to_draft(
    user_telegram_id: int,
    room_id: int,
    start_date,
    end_date
):
    user = User.objects.filter(
        telegram_id=user_telegram_id
    ).first()

    if not user:
        return None

    draft = ReservationDraft.objects.filter(
        user=user
    ).first()

    if not draft:
        draft = ReservationDraft.objects.create(
            user=user,
            room_id=room_id,
            start_date=start_date,
            end_date=end_date
        )
    else:
        draft.room_id = room_id
        draft.start_date = start_date
        draft.end_date = end_date
        draft.save()

    return draft


# Retrieves current reservation draft
@sync_to_async
def get_user_reservation_draft(user_telegram_id: int):
    return ReservationDraft.objects.filter(
        user__telegram_id=user_telegram_id
    ).select_related(
        'room'
    ).prefetch_related(
        'services'
    ).first()


# Deletes a user's reservation draft
@sync_to_async
def delete_reservation_draft(user_telegram_id: int):
    ReservationDraft.objects.filter(
        user__telegram_id=user_telegram_id
    ).delete()


# Processes booking after successful payment from reservation draft
@sync_to_async
def process_draft_payment_success(user_telegram_id: int):
    user = User.objects.filter(
        telegram_id=user_telegram_id
    ).first()

    if not user:
        return None

    draft = ReservationDraft.objects.filter(
        user=user
    ).select_related(
        'room'
    ).first()

    if not draft or not draft.room:
        return None

    rent_days = (draft.end_date - draft.start_date).days
    rent_days = max(rent_days, 1)

    total_price = draft.room.price * rent_days

    booking = Booking.objects.create(
        user=user,
        room=draft.room,
        start_date=draft.start_date,
        end_date=draft.end_date,
        rent_days=rent_days,
        total_price=total_price
    )

    draft.delete()

    return booking