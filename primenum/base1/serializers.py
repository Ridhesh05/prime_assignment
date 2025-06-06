from rest_framework import serializers

class PrimeCheckSerializer(serializers.Serializer):
    number = serializers.IntegerField(
        min_value=0,
        max_value=10**12,
        help_text="Number to check for primality (0 to 10^12)"
    )

class PrimeResponseSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    is_prime = serializers.BooleanField()
    message = serializers.CharField()
