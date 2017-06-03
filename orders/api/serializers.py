from rest_framework import serializers
from orders.models import BaseOrder, OrderItem, OrderPayment
from accounts.api.serializers import UserSerializer
from lands.models import Meta
from lands.api.serializers import MetaSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_api_url', read_only=True)
    product = MetaSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'url', 'product_name', 'product_code', 'product', 'unit_price', 'quantity', 'line_total']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = UserSerializer(read_only=True)
    url = serializers.CharField(source='get_api_url', read_only=True)
    class Meta:
        model = BaseOrder
        fields = ['id', 'url', 'customer', 'total', 'subtotal', 'status', 'is_valid','items']

class CreateOrderSerilzer(serializers.ModelSerializer):
    # pids = serializers.ListField( child=serializers.IntegerField(min_value=0) )

    class Meta:
        model = BaseOrder
        fields = ['id', 'total', 'subtotal']
        read_only_fields = ('id',)

    def validate(self, data):
        pids = self.context['request'].data['pids']
        if not pids:
            raise serializers.ValidationError('Please select land(s) and pass valid lands id list.')

        invalid_lands = []
        for pid in pids:
            qs = Meta.objects.filter(pk=pid)
            if not qs.exists():
                raise serializers.ValidationError('The land meta with id {land_id} does not exist'.format(land_id=pid))

            land = qs.first()
            if not land.is_active or land.is_rented:
                invalid_lands.append(land.id)

        if invalid_lands.__len__() > 0:
            raise serializers.ValidationError( 'The land meta with id(s) {lands} is not activated or has been rent'.
                                              format(lands=invalid_lands ) )

        return data

    def create(self, validated_data):
        total = validated_data.get('total', None)
        subtotal = validated_data.get('subtotal', None)
        pids = self.context['request'].data['pids']
        customer = self.context["request"].user
        instance = BaseOrder.objects.create(total=total, subtotal=subtotal, customer=customer)

        for pid in pids:
            product = Meta.objects.get(pk=pid)
            OrderItem.objects.create(
                order=instance,
                product=product,
                product_name=product.num,
                unit_price=product.price,
                line_total=product.price
            )
            # lock the product
            product.is_rented = True
            product.save()

        return instance