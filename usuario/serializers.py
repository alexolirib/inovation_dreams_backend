from rest_framework import serializers

class CriarUsuarioSerializar(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=15)
    profile = serializers.CharField(max_length=1)

    def validate(self, data):
        pass
