from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import ItemSerializer, OrderSerializer
from .models import Item , Order
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import (
        ListModelMixin,
        UpdateModelMixin,
        RetrieveModelMixin
    )


class ItemViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        viewsets.GenericViewSet
        ):
    """
    Conjunto de vistas simples para listar o recibir items.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class OrderViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        viewsets.GenericViewSet
        ):
    """
    Conjunto de vistas simples para listar, recibir y crear pedidos.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Retorna lista con todas las ordenes del usuario autentificado.
        """
        user = self.request.user
        return Order.objects.filter(user = user)

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = OrderSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                item = Item.objects.get(pk = data["item"])
                order = item.place_order(request.user, data["quantity"])
                return Response(OrderSerializer(order).data)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"},
                                status= 400)
