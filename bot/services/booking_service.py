from datetime import date, datetime, timedelta
from typing import Tuple


# Change selected number of rental days
def calculate_rent_days(current: int, delta: int, min_days: int = 1) -> int:
    return max(current + delta, min_days)


# Calculate accommodation cost
def calculate_price(price_per_day: int, days: int) -> int:
    return price_per_day * days


# Calculate days between dates
def get_rent_days(start_date: date, end_date: date, min_days: int = 1) -> int:
    return max((end_date - start_date).days, min_days)


# Calculate booking summary with days and total price
def calculate_booking_total(
    price_per_day: int,
    start_date: date,
    end_date: date
) -> Tuple[int, int]:
    rent_days = get_rent_days(start_date, end_date)
    total_price = calculate_price(price_per_day, rent_days)
    return rent_days, total_price


# Create booking dates from selected rental days
def get_dates(days: int) -> Tuple[date, date]:
    start = datetime.now().date()
    end = start + timedelta(days=days)
    return start, end
