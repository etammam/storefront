from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


def say_hello(request):
    return render(request,'hello.html', {'name': 'Eslam'})


@api_view()
def greeting(request):
    return Response('Hello World!')


@api_view()
def greeting_someone(request, name):
    return Response('hello ' + name)
