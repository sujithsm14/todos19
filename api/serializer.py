from rest_framework import serializers
from api.models import Todos
from django.contrib.auth.models import User


class TodoSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    class Meta:
        model=Todos
        fields=["id",
                "task_name",
                "user",
               "status"
        ]

    def create(self, validated_data):
        usr=self.context.get("user")
        return Todos.objects.create(**validated_data,user=usr)    
        

class RegistrationSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
   
    class Meta:
        model=User
        fields=[ "id",  
            "first_name",
                "last_name",             
                "username",
                "password",
                "email"
                ]
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)    
