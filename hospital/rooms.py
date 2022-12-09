from django.shortcuts import render,redirect
from django.http  import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import re,os

@login_required(login_url='/login/') 
def add_Room(request):
    if request.user.is_superuser == True:
        if request.method == "POST":
            room_type = request.POST['type']
            room_price = request.POST['price']
            bed_No = request.POST['bedlist']
            try:
                room_add_data=room(roomType=room_type,roomPrice=room_price)
                room_add_data.save()
                for i in range(int(bed_No)):
                    bed(bedStatus=False,roomId=room_add_data).save()
                messages.success(request,'Add Sucessfully')
            except:
                messages.error(request,'Type is allready axist')
            return render(request,'base.html')
        return render(request,'add_rooms.html')
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def view_Room(request):
    if request.user.is_superuser == True:
        room_data = room.objects.all().order_by('roomId')
        bed_data=bed.objects.all().order_by('bedId')          
        contex={
            'room_data':room_data,
            'bed_data':bed_data
        }
        return render(request,'add_rooms.html',contex)
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def update(request,id):
    if request.user.is_superuser == True:
        room_update_data=room.objects.get(roomId=id)
        if request.method == 'POST':
            room_type = request.POST['type']
            room_price = request.POST['price']
            room.objects.filter(roomId=id).update(
                roomType=room_type,
                roomPrice=room_price
            )
            messages.success(request,'Update Sucessfully')
            return render(request,'base.html')
        return render(request,'add_rooms.html',{'room_update_data':room_update_data})
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def delete(request,id):
    if request.user.is_superuser == True:
        room.objects.get(roomId=id).delete()
        messages.success(request,'Delete Sucessfully')
        return render(request,'base.html')
    return HttpResponseNotFound('Page Not Found')

