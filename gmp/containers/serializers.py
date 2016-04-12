from rest_framework import serializers

from .models import Container , Factory, Carrier, Material, Welding, Control


class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = ('name', )

    def to_representation(self, obj):
        return obj.name


class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = ('name', )

    def to_representation(self, obj):
        return obj.name


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('name', )

    def to_representation(self, obj):
        return obj.name


class WeldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Welding
        fields = ('name', 'material')


class ControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = ('name', 'area')



class ContainerSerializer(serializers.ModelSerializer):
    factory = FactorySerializer()
    carrier = CarrierSerializer()
    material_ring = MaterialSerializer()
    material_bottom = MaterialSerializer()
    welding = WeldingSerializer()
    control = ControlSerializer()
    full_desc = serializers.SerializerMethodField()
    full_desc_capital = serializers.SerializerMethodField()

    def get_full_desc(self, obj):
        return str(obj)

    def get_full_desc_capital(self, obj):
        return str(obj).capitalize()

    class Meta:
        model = Container
