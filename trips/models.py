from django.db import models


class Trip(models.Model):
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)

    current_cycle_used = models.FloatField()

    total_distance_miles = models.FloatField()
    total_duration_hours = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)


class DutyLog(models.Model):

    STATUS_CHOICES = [
        ("OFF", "Off Duty"),
        ("SB", "Sleeper Berth"),
        ("DRIVING", "Driving"),
        ("ON", "On Duty"),
    ]

    trip = models.ForeignKey(
        Trip,
        related_name="duty_logs",
        on_delete=models.CASCADE
    )

    day_number = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    start_hour = models.FloatField()
    end_hour = models.FloatField()
