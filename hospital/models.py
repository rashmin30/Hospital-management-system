from django.db import models
from django.contrib.auth.models import AbstractUser
from .models import *

class Lillnes(models.Model):
    lillne_id=models.AutoField(primary_key=True)
    lillne_name=models.CharField(max_length=255,default=None)

class room(models.Model):
    roomId=models.AutoField(db_column="Room_ID",primary_key=True)
    roomType=models.CharField(db_column="Room_Type",max_length=255,unique=True)
    roomPrice = models.IntegerField(db_column="Room_Price",blank=True,null=True)
    
    def __str__(self) :
        return self.roomType,self.roomId,self.roomPrice

class Medicines(models.Model):
    medicinesId=models.AutoField(db_column="Medicines_Id",primary_key=True)
    lillness = models.ForeignKey(Lillnes,on_delete=models.CASCADE,blank=True,null=True)
    medicinesName=models.CharField(db_column='Medicines_Name',max_length=255,unique=True)
    medicinesPrice=models.IntegerField(db_column='Medicines_Price')
    medicinesQuantity=models.IntegerField(db_column='Medicines_Quantity')

    def __str__(self) :
        return self.medicinesId,self.lillness,self.medicinesPrice,self.medicinesQuantity


class User(AbstractUser):
    lillness = models.ForeignKey(Lillnes,on_delete=models.CASCADE,blank=True,null=True)
    room=models.ForeignKey(room,on_delete=models.CASCADE,blank=True,null=True,db_column='Room_Id')
    medicines=models.ForeignKey(Medicines,on_delete=models.CASCADE,blank=True,null=True,db_column='Medicines_Id')
    medicinesQuantity = models.IntegerField(blank=True,null=True)
    fess = models.IntegerField(blank=True,null=True)
    category = models.CharField(max_length=255,blank=True,null=True)
    phone = models.BigIntegerField(blank=True,null=True)
    img = models.ImageField(upload_to='img',blank=True,null=True)
    doctor_id = models.IntegerField(blank=True,null=True)
    staff_id = models.IntegerField(blank=True,null=True)
    
    class Meta:
        db_table = 'auth_user'

class bed(models.Model):
    bedId=models.AutoField(db_column='Bed_Id',primary_key=True)
    bedStatus=models.CharField(db_column='Bed_Status',max_length=255, default=False)
    roomId=models.ForeignKey(room,on_delete=models.CASCADE,db_column='Room_Id')
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,db_column='User_Id',blank=True,null=True)
    
# class usesrMedicinesDetail(models.Model):
#     userId=models.ForeignKey(User,on_delete=models.CASCADE,db_column='User_Id',blank=True,null=True)
