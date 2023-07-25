from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=4, decimal_places=2)


class VendingMachineSlotSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    coordinates = serializers.SerializerMethodField()
    product = ProductSerializer()

    @staticmethod
    def get_coordinates(instance) -> list[int, int]:
        return [instance.row, instance.column]


class ClientSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.StringRelatedField()
    last_name = serializers.StringRelatedField()
    credit = serializers.DecimalField(max_digits=6, decimal_places=2)