from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages

@login_required(login_url='/login/')
def viewlillnes(request):
    if request.user.is_superuser == True:
        data_all_lillness = Lillnes.objects.all().order_by('lillne_name')
        return render(request,'addlillnes.html',{'data_lillness':data_all_lillness})
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def addlillnes(request):
    if request.user.is_superuser == True:
        if request.method == 'POST':
            lillne_name=request.POST['lillne']
            data_lillnes=Lillnes(lillne_name=lillne_name)
            data_lillnes.save()
            messages.success(request,'Insert Sucessfully')
            return render(request,'base.html')
        return render(request,'addlillnes.html')
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def update(request,id):
    if request.user.is_superuser == True:
        lillnes_data=Lillnes.objects.get(lillne_id=id)
        if request.method == 'POST':
            lillnes_data.lillne_name=request.POST['lillne']
            lillnes_data.save()
            messages.success(request,'Update Sucessfully')
            return render(request,'base.html')
            # return redirect('update-illnes',id=id)
        return render(request,'addlillnes.html',{'illness_data':lillnes_data})
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def delete(request,id):
    if request.user.is_superuser == True:
        Lillnes.objects.get(lillne_id=id).delete()
        messages.success(request,'Delete Sucessfully')
        return render(request,'base.html')
    return HttpResponseNotFound('Page Not Found')

