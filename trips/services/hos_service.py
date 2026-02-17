import math


class ELDService:

    MAX_DRIVE = 11
    MAX_ON_DUTY = 14
    MAX_CYCLE = 70
    BREAK_AFTER = 8
    RESET_HOURS = 10
    FUEL_INTERVAL = 1000

    @classmethod
    def generate_logs(cls, total_drive, total_miles, cycle_used):

        day_number = 1
        remaining_drive = total_drive
        remaining_cycle = cls.MAX_CYCLE - cycle_used
        fuel_stops = math.floor(total_miles / cls.FUEL_INTERVAL)

        all_days = []

        while remaining_drive > 0 and remaining_cycle > 0:

            logs = []
            current_hour = 0
            driving_today = 0
            on_duty_today = 0
            took_break = False

            # Pickup first day
            if day_number == 1:
                logs.append(("ON", current_hour, current_hour + 1))
                current_hour += 1
                on_duty_today += 1

            while (
                driving_today < cls.MAX_DRIVE
                and on_duty_today < cls.MAX_ON_DUTY
                and remaining_drive > 0
                and remaining_cycle > 0
            ):

                # 30-min break after 8 hrs
                if driving_today >= cls.BREAK_AFTER and not took_break:
                    logs.append(("ON", current_hour, current_hour + 0.5))
                    current_hour += 0.5
                    on_duty_today += 0.5
                    took_break = True

                drive_chunk = min(
                    cls.MAX_DRIVE - driving_today,
                    remaining_drive
                )

                logs.append(("DRIVING", current_hour, current_hour + drive_chunk))

                current_hour += drive_chunk
                driving_today += drive_chunk
                on_duty_today += drive_chunk
                remaining_drive -= drive_chunk
                remaining_cycle -= drive_chunk

                # Fuel stop
                if fuel_stops > 0:
                    logs.append(("ON", current_hour, current_hour + 0.5))
                    current_hour += 0.5
                    on_duty_today += 0.5
                    fuel_stops -= 1

            # Dropoff final day
            if remaining_drive <= 0:
                logs.append(("ON", current_hour, current_hour + 1))
                current_hour += 1

            # Off-duty remainder
            if current_hour < 24:
                logs.append(("OFF", current_hour, 24))

            all_days.append({
                "day": day_number,
                "logs": logs
            })

            day_number += 1

        return all_days
