from rest_framework import generics, status, permissions, viewsets
from orders.models import BaseOrder, OrderItem, OrderPayment
from .serializers import OrderSerializer, CreateOrderSerilzer, OrderItemSerializer
from rest_framework.response import Response
from accounts.permissions import IsOwnerOrReadOnly

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = BaseOrder.objects.all()
    serializer_class = CreateOrderSerilzer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        created_instance = BaseOrder.objects.get(pk=serializer.data['id'])
        order_detail_serializer = OrderSerializer(created_instance, context={request: request})

        return Response(data=order_detail_serializer.data, status=status.HTTP_201_CREATED)

class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return BaseOrder.objects.filter(customer = self.request.user)


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = BaseOrder.objects.filter(pk__gte=0)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.filter(pk__gte=0)