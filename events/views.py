from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

from rest_framework import mixins
from rest_framework import generics

from events.models import Todos
from events.serializers import RegistartionSerializer, TodoSerilarizer
from events.custompermissions import IsOwnerPermission

# ViewSet implementation
# ------------------------------------------------------------------------------------
class TodosView(ViewSet):

# to get the todolist

    def list(self,request,*args,**kwargs):
        qs=Todos.objects.all()
        serializer=TodoSerilarizer(qs,many=True)
        return Response(data=serializer.data)

# to create todos

    def create(self,request,*args,**kwargs):
        serializer=TodoSerilarizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

# to retrive todos 

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=TodoSerilarizer(qs,many=False)
        return Response(data=serializer.data)

# to delete todo 

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todos.objects.get(id=id).delete()
        return Response(data="Item Deleted")

# to update todo

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Todos.objects.get(id=id)
        serializer=TodoSerilarizer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

# --------------------------------------------------------------------------------
# model viewset have built-in implements of view set 
# so it can extract from that class-method

class TodosModelViews(ModelViewSet):
    http_method_names=["post","get","put"]
    # authentication and permissions
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=TodoSerilarizer
    queryset=Todos.objects.all()    # list the todos

    def get_queryset(self):  
        return Todos.objects.filter(user=self.request.user)  # overriding the list

    # def list(self,request,*args,**kwargs):  
    #     qs=Todos.objects.filter(user=request.user)
    #     serializer=TodoSerilarizer(qs,many=True)
    #     return Response(data=serializer.data)  
# only login user can access the user created task

# to pass task and user details to the srever

    # def perform_create(self, serializer):
    #     return serializer.save(user=self.request.user)  # to override create

# example: to take reviews then below code is need to run for all users

    def create(self,request,*args,**kwargs):
        serializer=TodoSerilarizer(data=request.data)
        if serializer.is_valid():
            Todos.objects.create(**serializer.validated_data,context={"user":request.user})  # (user=request.user) for normal case
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    @action(methods=['GET'],detail=False)      # list the pending todos
    def pending_todo(self,request,*args,**kwargs):
        qs=Todos.objects.filter(status=False,user=self.request.user)
        serializer=TodoSerilarizer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=['GET'],detail=False)      # list the completed todos
    def completed_todos(self,request,*args,**kwargs):
        qs=Todos.objects.filter(status=True,user=self.request.user)
        serializer=TodoSerilarizer(qs,many=True)
        return Response(data=serializer.data)
 
    @action(methods=['POST'],detail=True)     # to mark as read - updating list
    def mark_as_read(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id)
        qs.status=True
        qs.save()
        serializer=TodoSerilarizer(qs,many=False)
        return Response(data=serializer.data)

class UserView(ModelViewSet):
    serializer_class=RegistartionSerializer
    queryset=User.objects.all()

# encrypting the password

    # def create(self, request, *args, **kwargs):
    #     serializer=RegistartionSerializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

# the code to encrypt the password is lengthy 
# so it can be defaulty call from Model serializer
# therefore the method is implemneted in serializer.py
 
# update

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Todos.objects.get(id=id)
        serializer=RegistartionSerializer(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class TodoDeleteView(mixins.DestroyModelMixin,generics.GenericAPIView):
    serializer_class=TodoSerilarizer
    queryset=Todos.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def delete(self,request,*args,**kw):
        return self.destroy(request,*args,**kw)