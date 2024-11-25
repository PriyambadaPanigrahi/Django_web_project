from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import JsonResponse
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from django.http import HttpResponse
from django.shortcuts import render

import requests



def home(request):
    return HttpResponse("Welcome to the Home Page!")

# Account CRUD
class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


# Destination CRUD
class DestinationListCreateView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class DestinationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


# Get destinations by account_id
class AccountDestinationsView(APIView):
    def get(self, request, account_id):
        try:
            destinations = Destination.objects.filter(account__account_id=account_id)
            serializer = DestinationSerializer(destinations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)


# Handle incoming data
class DataHandlerView(APIView):
    def post(self, request):
        token = request.headers.get("CL-X-TOKEN")
        if not token:
            return Response({"error": "Unauthenticate"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            account = Account.objects.get(app_secret_token=token)
        except Account.DoesNotExist:
            return Response({"error": "Unauthenticate"}, status=status.HTTP_401_UNAUTHORIZED)

        for destination in account.destinations.all():
            headers = destination.headers
            if destination.http_method == "GET":
                requests.get(destination.url, headers=headers, params=request.data)
            elif destination.http_method in ("POST", "PUT"):
                requests.request(destination.http_method, destination.url, headers=headers, json=request.data)

        return Response({"status": "Data forwarded"}, status=status.HTTP_200_OK)

