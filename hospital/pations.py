from django.shortcuts import render,redirect
from django.http  import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import re,os

@login_required(login_url='/login/')
def add_pations(request):
    if request.user.is_superuser == True:
        user_data=User()
        data_illness = Lillnes.objects.all()
        if 'add_pations' in request.POST:
            password=request.POST['password']
            repassword=request.POST['repassword']
            if password != repassword:
                messages.error(request,'Password Not Match?')
                return render(request,'add_pations.html')
            conform_password = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$", password)
            if conform_password is None:
                messages.error(request,'Password Not Valid?')
                return render(request,'add_pations.html')
            user_data.username=request.POST['username']
            user_data.first_name=request.POST['fname']
            user_data.last_name=request.POST['lname']
            user_data.email=request.POST['email']
            user_data.phone=request.POST['phone']
            user_data.img=request.FILES['img']
            user_data.category=request.POST['category']
            user_data.set_password(password)
            selected_illness_name = request.POST['lillness']
            for i_illnes in data_illness:
                if i_illnes.lillne_name == selected_illness_name:
                    user_data.lillness=i_illnes
                    user_data.save()
            messages.success(request,'Add Pation Sucess')
            return render(request,'base.html')
        return render(request,'add_pations.html',{'data':data_illness})
    return HttpResponseNotFound('Page Not Found')


@login_required(login_url='/login/')
def view_pations(request):
    if request.user.is_superuser == True:    
        pations_view_data=User.objects.filter(category='P').order_by('id')
        return render(request,'view_pations.html',{'pations_data':pations_view_data})
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def update(request,id):
    if request.user.is_superuser == True:    
        pation_data=User.objects.get(id=id)
        data_illness = Lillnes.objects.all()
        if 'update_pations' in request.POST:
            if len(request.FILES) != 0:
                if len(pation_data.img) > 0:
                    os.remove(pation_data.img.path)
                    pation_data.img=request.FILES['img']
            pation_data.username=request.POST['username']
            pation_data.first_name=request.POST['fname']
            pation_data.last_name=request.POST['lname']
            pation_data.email=request.POST['email']
            pation_data.phone=request.POST['phone']
            pation_data.is_active = request.POST['block']
            selected_illness_name = request.POST['lillness']        
            for i_illnes in data_illness:
                if i_illnes.lillne_name == selected_illness_name:
                    pation_data.lillness=i_illnes
                    pation_data.save()
            messages.success(request,'Update Sucessfully')
            return render(request,'base.html')
        contex={
            'pation_data':pation_data,
            'data':data_illness
        }
        return render(request,'add_pations.html',contex)
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def Home(request):
    if request.user.category == 'P':
        illness=request.user.lillness.lillne_id
        pation_id=request.user.id
        data_doctor = User.objects.filter(is_superuser = False,is_staff = True,lillness=illness).order_by('fess')
        room_data = room.objects.all()
        bed_data = bed.objects.filter(user_id=pation_id)
        if 'doc_id' in request.GET:
            selected_doctor_id=request.GET['doc_id']
            User.objects.filter(id=pation_id).update(doctor_id=selected_doctor_id)
            return redirect('pation-Home')
        elif 'staff_id' in request.GET:
            selected_staff_id=request.GET['staff_id']
            User.objects.filter(id=pation_id).update(staff_id=selected_staff_id)
            return redirect('pation-Home')
        elif request.method == 'POST':
            if request.user.doctor_id == "" or request.user.doctor_id == None :
                messages.error(request,'Select Docotor ')
            elif request.user.staff_id == None or request.user.staff_id == "":
                messages.error(request,'Select Staff ')
            else:
                select_room = request.POST['select_room']
                User.objects.filter(id=pation_id).update(room=select_room)
            return redirect('pation-Home')
        contex={
            'data':data_doctor,
            'room_data':room_data,
            'bed_data':bed_data
        }
        return render(request,'pation_home.html',contex)
    return HttpResponseNotFound('Page Not Found')

