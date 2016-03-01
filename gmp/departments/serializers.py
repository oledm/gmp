from rest_framework import serializers

from .models import Instrument

class InstrumentSeriazlier(serializers.ModelSerializer):
    
    class Meta:

        model = Instrument
