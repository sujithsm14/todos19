from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet,ModelViewSet
from api.models import Todos
from api.serializer import TodoSerializer,RegistrationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

class TodosViews(ViewSet):
    def list(self,request,*args,**kw):
        qs=Todos.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Todos.objects.filter(id=id)
        serializer=TodoSerializer(qs,many=False)
        return Response(data=serializer.data)    
    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        Todos.objects.filter(id=id).delete()
        return Response(data="deleted")
    def update(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class TodoModelView(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]



    serializer_class=TodoSerializer
    queryset=Todos.objects.all()


    def list(self, request, *args, **kwargs):
        qs=Todos.objects.filter(user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    # def create(self, request, *args,**kw):
    #     serializer=TodoSerializer(data=request.data)

    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer.validated_data,user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False, user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["GET"],detail=False)
    def completed_Todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False,user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["post"],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        #object=Todos.objects.filter(id=id).update(status=False)
        object=Todos.objects.get(id=id)
        object.status=True
        object.save()
        serializer=TodoSerializer(object,many=False)
        return Response(data=serializer.data)
    

class UserView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()


   # def create(self, request, *args, **kwargs):
    #    serializer=RegistrationSerializer(data=request.data)
     #   if serializer.is_valid():
      #      qs=User.objects.create_user(**serializer.validated_data)
       #     return Response(data=serializer.data)
      #  else:
       #     return Response(data=serializer.errors)


