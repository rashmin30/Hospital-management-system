from django.urls import path,include
from . import views
from . import doctor,lillnes,staff,pations,rooms,medicines

urlpatterns = [
    # home for Login
    path('',views.index,name='index'),
    path('login/',views.user_login,name='Login'),
    path('logout/',views.user_logout,name='logout'),


    #doctor Urls,
    path('adddoctor/',doctor.adddoctor,name='add-doctor'),
    path('viewdoctor/',doctor.viewdoctor,name='view-doctor'),
    path('viewdoctor/update/<int:id>',doctor.update,name='update_doctor'),
    path('viewdoctor/delete/<int:id>',doctor.delete,name='delete_doctor'),
    path('doctor-Home/',doctor.Home,name='doctor-Home'),
    path('apply-medicines/<int:m_id>/<int:user_id>',doctor.apply_Mediciens,name='apply-medicines'),

    #Staff Urls
    path('addstaff/',staff.addstaff,name='add-staff'),
    path('viewstaff/',staff.viewstaff,name='view-staff'),
    path('viewstaff/update/<int:id>',staff.update,name='update_staff'),
    path('viewstaff/delete/<int:id>',doctor.delete,name='delete_staff'),
    path('staff-Home/',staff.Home,name='staff-Home'),
    path('staff-Home/<int:roomid>/<int:userid>',staff.roomSelect,name='Room-Select'),
    path('pation-Home/change_room/<int:roomid>/<int:userid>',staff.changeroom,name='change-Rooms'),

    #Pation Urls
    path('add-pations/',pations.add_pations,name='add-pations'),
    path('view-pations/',pations.view_pations,name='view-pations'),
    path('view-pations/update/<int:id>',pations.update,name='update-pations'),
    path('view-pations/delete/<int:id>',doctor.delete,name='delete-pations'),
    path('pation-Home/',pations.Home,name='pation-Home'),

    #Illness Urls
    path('addlillnes/',lillnes.addlillnes,name='Add-illnes'),
    path('viewlillnes/',lillnes.viewlillnes,name='view-illnes'),
    path('viewlillnes/update/<int:id>',lillnes.update,name='update-illnes'),
    path('viewlillnes/delete/<int:id>',lillnes.viewlillnes,name='delete-illnes'),

    #room Urls
    path('add_Room/',rooms.add_Room,name='Add-Rooms'),
    path('view_add_Room/',rooms.view_Room,name='View-Rooms'),
    path('view_add_Room/update/<int:id>',rooms.update,name='View-Rooms'),
    path('view_add_Room/delete/<int:id>',rooms.delete,name='View-Rooms'),

    #Medicines Urls
    path('add_medicine/',medicines.add_medicines,name='Add-Medicines'),
    path('view_medicine/',medicines.veiw_medicines,name='view-Medicines'),
    path('view_medicine/update/<int:id>',medicines.update,name='update-Medicines'),
    path('view_medicine/delete/<int:id>',medicines.delete,name='delete-Medicines'),
]