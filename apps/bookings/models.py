from django.db import models
from apps.users.models import User
from apps.rooms.models import Room


class Booking(models.Model):
    # Foreign keys with cascade deletion
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Пользователь"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Номер"
    )
    # Booking dates and cost details
    start_date = models.DateField(verbose_name="Дата заезда")
    end_date = models.DateField(verbose_name="Дата выезда")
    rent_days = models.IntegerField(verbose_name="Количество дней проживания")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая стоимость"
    )

    # String representation for admin panel
    def __str__(self):
        return f"Бронирование #{self.id} — Номер {self.room.room_number} ({self.user})"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"


class ReservationDraft(models.Model):
    # Foreign keys with cascade deletion
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservation_drafts',
        verbose_name="Пользователь"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='reservation_drafts',
        verbose_name="Номер"
    )

    # Reservation dates
    start_date = models.DateField(verbose_name="Дата заезда")
    end_date = models.DateField(verbose_name="Дата выезда")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    # Related services
    services = models.ManyToManyField(
        'Service',
        through='ReservationDraftService',
        related_name='reservation_drafts'
    )

    # String representation for admin panel
    def __str__(self):
        return f"Черновик бронирования #{self.id}"

    class Meta:
        verbose_name = "Черновик бронирования"
        verbose_name_plural = "Черновики бронирований"
        unique_together = ('user', 'room', 'start_date', 'end_date')


class Service(models.Model):
    # Service details
    name = models.CharField(max_length=255, verbose_name="Название услуги")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость"
    )

    # String representation for admin panel
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class ReservationDraftService(models.Model):
    # Foreign keys with cascade deletion
    reservation_draft = models.ForeignKey(
        ReservationDraft,
        on_delete=models.CASCADE,
        related_name='draft_services',
        verbose_name="Черновик бронирования"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='draft_services',
        verbose_name="Услуга"
    )

    # String representation for admin panel
    def __str__(self):
        return f"{self.reservation_draft} - {self.service}"

    class Meta:
        verbose_name = "Услуга черновика бронирования"
        verbose_name_plural = "Услуги черновиков бронирования"
        unique_together = ('reservation_draft', 'service')
