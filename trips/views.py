from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import TripSerializer
from .models import Trip, DutyLog
from .services.route_service import RouteService
from .services.hos_service import ELDService


class TripView(APIView):

    def post(self, request):

        serializer = TripSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data

        try:
            start = RouteService.geocode(data["current_location"])
            pickup = RouteService.geocode(data["pickup_location"])
            dropoff = RouteService.geocode(data["dropoff_location"])

            route = RouteService.get_route(start, pickup, dropoff)

            eld_days = ELDService.generate_logs(
                route["duration_hours"],
                route["distance_miles"],
                data["current_cycle_used"]
            )

            trip = Trip.objects.create(
                current_location=data["current_location"],
                pickup_location=data["pickup_location"],
                dropoff_location=data["dropoff_location"],
                current_cycle_used=data["current_cycle_used"],
                total_distance_miles=route["distance_miles"],
                total_duration_hours=route["duration_hours"],
            )

            # Save logs
            for day in eld_days:
                for status_code, start_hour, end_hour in day["logs"]:
                    DutyLog.objects.create(
                        trip=trip,
                        day_number=day["day"],
                        status=status_code,
                        start_hour=start_hour,
                        end_hour=end_hour
                    )

            # Response formatting
            response_logs = []
            for day in eld_days:
                response_logs.append({
                    "day": day["day"],
                    "logs": [
                        {
                            "status": s,
                            "start": st,
                            "end": en
                        }
                        for s, st, en in day["logs"]
                    ]
                })

            return Response({
                "trip_id": trip.id,
                "summary": {
                    "total_distance": route["distance_miles"],
                    "total_duration": route["duration_hours"],
                },
                "geometry": route["geometry"],
                "steps": route["steps"],
                "eld_logs": response_logs,
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
