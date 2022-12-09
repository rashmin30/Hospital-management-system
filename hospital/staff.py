from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import re,os


@login_required(login_url='/login/')
def addstaff(request):
    if request.user.is_superuser == True:
        user_data = User()
        data_illness = Lillnes.objects.all()
        if request.method == 'POST':
            password=request.POST['password']
            repassword=request.POST['repassword']
            if password != repassword:
                messages.error(request,'Password Not Match?')
                return render(request,'addstaff.html',{'data':data_illness})
            conform_password = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$", password)
            if conform_password is None:
                messages.error(request,'Password Not Valid?')
                return render(request,'addstaff.html',{'data':data_illness})
            user_data.set_password(password)
            user_data.username=request.POST['username']
            user_data.first_name=request.POST['fname']
            user_data.last_name=request.POST['lname']
            user_data.email=request.POST['email']
            user_data.phone=request.POST['phone']
            user_data.img=request.FILES['img']
            user_data.fess=request.POST['fess']
            user_data.category=request.POST['category']
            selected_illness_name = request.POST['lillness']
            user_data.is_staff = True
            for i_illnes in data_illness:
                if i_illnes.lillne_name == selected_illness_name:
                    user_data.lillness=i_illnes
                    user_data.save()
            messages.success(request,'Insert Sucessfully')
            return render(request,'base.html')
        return render(request,'addstaff.html',{'data':data_illness})
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def viewstaff(request):
    if request.user.is_superuser == True:
        staff_data = User.objects.filter(category="S").order_by('id')
        return render(request,'viewstaff.html',{'staff_data':staff_data})
    return HttpResponseNotFound('Page Not Found')


@login_required(login_url='/login/')
def update(request,id):
    if request.user.is_superuser == True:
        staff_data=User.objects.get(id=id)
        data_illness = Lillnes.objects.all()
        if 'update_staff' in request.POST:
            if len(request.FILES) != 0:
                if len(staff_data.img) > 0:
                    os.remove(staff_data.img.path)
                    staff_data.img=request.FILES['img']
            staff_data.username=request.POST['username']
            staff_data.first_name=request.POST['fname']
            staff_data.last_name=request.POST['lname']
            staff_data.email=request.POST['email']
            staff_data.phone=request.POST['phone']
            selected_illness_name = request.POST['lillness']        
            staff_data.is_active = request.POST['block']
            staff_data.fess = request.POST['fess']
            for i_illnes in data_illness:
                if i_illnes.lillne_name == selected_illness_name:
                    staff_data.lillness=i_illnes
                    staff_data.save()
            messages.success(request,'Update Sucessfully')
            return render(request,'base.html')
        contex={
            'staff_data':staff_data,
            'data':data_illness
        }
        return render(request,'addstaff.html',contex)
    return HttpResponseNotFound('Page Not Found')

@login_required(login_url='/login/')
def Home(request):
    if request.user.category == 'S':
        pations_data = User.objects.filter(category="P").order_by('id')
        check_bed_in_user=bed.objects.filter(bedStatus=True).order_by('bedId')
        contex={
            'pations_data':pations_data,
            'check_bed_in_user':check_bed_in_user
        }
        return render(request,'staff_Home.html',contex)
    return HttpResponseNotFound('Page Not Found') 


@login_required(login_url='/login/')
def roomSelect(request,roomid,userid):
    if request.user.category == 'S':
        pations_data = User.objects.get(id=userid)
        bed_data = bed.objects.filter(roomId=roomid).order_by('bedId')
        user_len=bed_data.filter(user_id=userid)
        if 'select_bed' in request.POST:
            bed_id = request.POST['book_bed']
            try:
                for i in bed_data:
                    if len(user_len) == 0:
                        if i.bedId == int(bed_id):
                            i.user_id=pations_data
                            i.bedStatus=True
                            i.save()
                            messages.success(request,f'Bed No Apply :{int(bed_id)}')
                            return redirect('staff-Home')
                    else:
                        messages.error(request,f'Bed allready Selected Room : {user_len[0].roomId.roomType} OR Bed No :{user_len[0].bedId}')
                        return redirect('staff-Home')
            except:
                messages.error(request,'Not Select More Bed')
            return redirect('staff-Home')
        contex={
            'pations_data':pations_data,
            'bed_data':bed_data
        }
        return render(request,'Rooms.html',contex)
    return HttpResponseNotFound('Page Not Found') 

def changeroom(request,roomid,userid):
    User.objects.filter(id=userid).update(
        room=""
    )
    bed.objects.filter(user_id=userid).update(
        user_id="",
        bedStatus=False
    )
    return redirect('pation-Home')