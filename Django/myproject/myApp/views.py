from django.shortcuts import render
from .models import Travel

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def create_travel(request):
    if request.method == 'POST':
        Travel.objects.create(
            has_traveled_toeurope=request.data.get("has_traveled_toeurope"),
            contries=request.data.get("countries"),
        )

        return Response({
            "message": "Travel Created",
        })

    if request.method == 'GET':
        travel = Travel.objects.last()

        if not travel:
            return Response({"message": "No data found"})

        return Response({
            "has_traveled_toeurope": travel.has_traveled_toeurope,
            "countries": travel.contries,
        })