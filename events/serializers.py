from rest_framework import serializers
from events.models import Todos
from django.contrib.auth.models import User

# todo list fields 

class TodoSerilarizer(serializers.ModelSerializer):
    status=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Todos
        fields=["task_name","user","status"]

# importing create method for views

    def create(self,validated_data):
        usr=self.context.get("user")
        return Todos.objects.create(**validated_data,user=usr)

# for user registartion to authorize the person and for encryption

class RegistartionSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","username","password","email"]

# create method calling from Model serializers
 
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)