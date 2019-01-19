from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
import requests
from myApp.models import food

def objTofood(donnee,sum):
    return food(starter_name=donnee["starter"]["display_name"],dish_name=donnee["dish"]["display_name"],desert_name=donnee["desert"]["display_name"]
    ,starter_calories=donnee["starter"]["cal"],dish_calories=donnee["dish"]["cal"],desert_calories=donnee["desert"]["cal"],sum_calories=sum)

# Create your views here.

headers = {'Authorization': 'Bearer iwn-31@!3pf(w]pmarewj236^in'}

def home(request):
    response = requests.get('https://foodvisor.io/itw/food/list/?foo=bar', headers=headers)
    fooddata = response.json()
    #return JsonResponse(fooddata, safe=False)
    return render(request, 'foods.html', {'foods': fooddata })

@api_view(["POST"])
def FoodResponse(foodData):
    try:
        #defining variables
        calMoy=500
        percentage=0.1
        calSum=0
        starter = (json.loads(json.dumps(foodData.data["starter"])))
        dish = json.loads(json.dumps(foodData.data["dish"]))
        desert = json.loads(json.dumps(foodData.data["desert"]))
        if (type(starter) == type("string")):
            starter=json.loads(starter)
            dish=json.loads(dish)
            desert=json.loads(desert)
        donnee = {"starter":starter, "dish":dish, "desert":desert}
        #print(donnee)
        calSum= calSum + starter["cal"]+ dish["cal"]+ desert["cal"]
        objTofood(donnee,calSum).save()
        if ( (calSum < calMoy*(1-percentage)) or (calSum > calMoy*(1+percentage)) ):
            return JsonResponse({
            "status": "KO",
            "food": donnee
            })
        else:
            return JsonResponse({
            "status": "OK",
            "food": donnee
            })
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def interface(foodData):
    try:
        #defining variables
        calMoy=500
        percentage=0.1
        calSum=0
        starter = (json.loads(json.dumps(foodData.data["starter"])))
        dish = json.loads(json.dumps(foodData.data["dish"]))
        desert = json.loads(json.dumps(foodData.data["desert"]))
        if (type(starter) == type("string")):
            starter=json.loads(starter)
            dish=json.loads(dish)
            desert=json.loads(desert)
        donnee = {"starter":starter, "dish":dish, "desert":desert}
        #print(donnee)
        calSum= calSum + starter["cal"]+ dish["cal"]+ desert["cal"]
        objTofood(donnee,calSum).save()
        if ( (calSum < calMoy*(1-percentage)) or (calSum > calMoy*(1+percentage)) ):
            return render(foodData,"choix.html", {
            "status": "KO",
            "food": donnee,
            "somme":calSum
            })
        else:
            return render(foodData,"choix.html",{
            "status": "OK",
            "food": donnee,
            "somme":calSum
            })
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
