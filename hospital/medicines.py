from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

@login_required(login_url='/login/')
def add_medicines(request):
    if request.user.is_superuser == True:   
        data_illness = Lillnes.objects.all()
        if request.method == 'POST':
            illnes=request.POST['lillness']
            medicinename=request.POST['medicinename']
            medicineprice=request.POST['medicineprice']
            medicinequantity=request.POST['medicinequantity']
            illnes_id=data_illness.get(lillne_id=illnes)
            try:
                mediciens_data=Medicines(lillness=illnes_id,medicinesName=medicinename,medicinesPrice=medicineprice,medicinesQuantity=medicinequantity)
                mediciens_data.save()
                messages.success(request,'Medicines Add Sucessfully')
            except:
                messages.error(request,'Medicines Allrady Added')
            return render(request,'base.html')
        contax={
            'data_illness':data_illness
        }
        return render(request,'Medicines/add_medicine.html',contax)
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def veiw_medicines(request):
    if request.user.is_superuser == True:   
        Medicines_data=Medicines.objects.all().order_by('medicinesId')
        return render(request,'Medicines/view_medicines.html',{'medicines_data':Medicines_data})
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def update(request,id):
    if request.user.is_superuser == True:
        data_illness = Lillnes.objects.all()
        medicines_data=Medicines.objects.get(medicinesId=id)
        if request.method == 'POST':
            try:
                medicines_data.lillness=data_illness.get(lillne_id=request.POST['lillness'])
                medicines_data.medicinesName=request.POST['medicinename']
                medicines_data.medicinesPrice=request.POST['medicineprice']
                medicines_data.medicinesQuantity=request.POST['medicinequantity']
                medicines_data.save()
                messages.success(request,'Update Sucessfully')
            except:
                messages.error(request,'Medicines Allrady Added')
            return redirect('view-Medicines')
        contex={
            'data_illness':data_illness,
            'medicines_data':medicines_data
        }
        return render(request,'Medicines/add_medicine.html',contex)
    return HttpResponseNotFound('Page Not Found')


@login_required(login_url='/login/')
def delete(request,id):
    if request.user.is_superuser == True:
        Medicines.objects.get(medicinesId=id).delete()
        messages.success(request,'Delete Sucessfully')
        return render(request,'base.html')
    return HttpResponseNotFound('Page Not Found')