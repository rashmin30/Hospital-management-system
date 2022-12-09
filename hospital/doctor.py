from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import re,os
from django.db.models import Q

@login_required(login_url='/login/')
def adddoctor(request):
    if request.user.is_superuser == True:
        user_data = User()
        data_illness = Lillnes.objects.all()
        if request.method == 'POST':
            password=request.POST['password']
            repassword=request.POST['repassword']
            if password != repassword:
                messages.error(request,'Password Not Match?')
                return render(request,'adddoctor.html',{'data':data_illness})
            conform_password = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$", password)
            if conform_password is None:
                messages.error(request,'Password Not Valid?')
                return render(request,'adddoctor.html',{'data':data_illness})
            user_data.set_password(password)
            user_data.username=request.POST['username']
            user_data.first_name=request.POST['fname']
            user_data.last_name=request.POST['lname']
            user_data.email=request.POST['email']
            user_data.phone=request.POST['phone']
            user_data.fess=request.POST['fess']
            user_data.img=request.FILES['img']
            user_data.category=request.POST['category']
            selected_illness_name = request.POST['lillness']
            user_data.is_staff = True
            for i_illnes in data_illness:   
                if i_illnes.lillne_name == selected_illness_name:
                    user_data.lillness=i_illnes
                    user_data.save()
            messages.success(request,'Insert Sucessfully')
            return render(request,'base.html')
        return render(request,'adddoctor.html',{'data':data_illness})
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def viewdoctor(request):
    if request.user.is_superuser == True:
        doctor_data = User.objects.filter(category="D").order_by('lillness')
        return render(request,'viewdoctor.html',{'doctor_data':doctor_data})
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def update(request,id):
    if request.user.is_superuser == True:
        doc_data=User.objects.get(id=id)
        data_illness = Lillnes.objects.all()
        if 'update_doctor' in request.POST:
            if len(request.FILES) != 0:
                if len(doc_data.img) > 0:
                    os.remove(doc_data.img.path)
                    doc_data.img=request.FILES['img']
            doc_data.username=request.POST['username']
            doc_data.first_name=request.POST['fname']
            doc_data.last_name=request.POST['lname']
            doc_data.email=request.POST['email']
            doc_data.phone=request.POST['phone']
            doc_data.fess=request.POST['fess']
            selected_illness_name = request.POST['lillness']
            doc_data.is_active = request.POST['block']
            for i_illnes in data_illness:
                if i_illnes.lillne_name == selected_illness_name:
                    doc_data.lillness=i_illnes
                    doc_data.save()
            messages.success(request,'Update Sucessfully')
            return render(request,'base.html')
        contex={
            'doc_data':doc_data,
            'data':data_illness
        }
        return render(request,'adddoctor.html',contex)
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def delete(request,id):
    if request.user.is_superuser == True:
        User.objects.get(id=id).delete()
        messages.danger(request,'Delete Sucessfully')
        return render(request,'base.html')
    return HttpResponseNotFound('Page Not Found')


@login_required(login_url='/login/')
def Home(request):
    if request.user.category == 'D':
        doctor_illness=request.user.lillness
        id = request.user.id
        pation_staff_data = User.objects.filter(Q(lillness=doctor_illness) & Q(category='S') | Q(lillness=doctor_illness) & Q(doctor_id=id))
        bed_data = bed.objects.all()
        contex={
            'pation_staff_data':pation_staff_data,
            'bed_No':bed_data
        }
        return render(request,'Doctor/Doctor_Home.html',contex)
    return HttpResponseNotFound('Page Not Found') 

@login_required(login_url='/login/')
def apply_Mediciens(request,m_id,user_id):
    medicines_data=Medicines.objects.filter(lillness=m_id)
    if request.method == 'POST':
        medicines_id=int(request.POST['medicineid'])
        medicines_quantity=int(request.POST['medicinequantity'])
        for i in medicines_data:
            if i.medicinesId == medicines_id:
                i.medicinesQuantity=i.medicinesQuantity - medicines_quantity
                if i.medicinesQuantity < 0 :
                    messages.error(request,f'Not Avilabel Medicines:{i.medicinesName}')
                i.save()
                User.objects.filter(id=user_id).update(
                    medicines=i,
                    medicinesQuantity = medicines_quantity
                )
                messages.success(request,'Send Mediciens')
                return redirect('doctor-Home')
    contex={
        'medicines_data':medicines_data
    }
    return render(request,'Doctor/apply_medicines.html',contex)