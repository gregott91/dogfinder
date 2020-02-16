from django.http import HttpResponse
from django.shortcuts import render
from pawscrawler import petcache
from pawscrawler.serializers import PetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

def index(request):
    pets = petcache.get_cached_pets()
    return render(request, 'doglist.html', {'pets': pets})

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class PetStatus(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        petcache.update_pet_status(request.data['id'], request.data['status'])
        return Response(status=status.HTTP_200_OK)