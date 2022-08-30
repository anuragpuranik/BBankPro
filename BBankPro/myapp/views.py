from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import *
from .forms import *
from django.contrib.auth import logout


def home(request):
    return render(request,'home.html')

class AddBloodBank(View):
    def get(self,request):
        myform=BloodbankForm()
        username=request.session['username']
        return render(request,'addBank.html',{'myform':myform,'username':username})        
    def post(self,request):
        unm=request.session['username']
        # print("The username is : ",unm)
        myform=BloodbankForm(request.POST)
        if myform.is_valid():
            bloodbankid=myform.cleaned_data['bloodbankid']
            bbname=myform.cleaned_data['bbname']
            address=myform.cleaned_data['address']
            city=myform.cleaned_data['city']
            contact=myform.cleaned_data['contact']
            email=myform.cleaned_data['email']
            contactPerson=myform.cleaned_data['contactPerson']
            username=unm
            bank=Bloodbank(bloodbankid,bbname,address,city,contact,email,contactPerson,username)
            bank.save()
            return redirect('home')
        else:
            return HttpResponse("<h5>Data could not be added...")          
 
def bankList(request):
    data=Bloodbank.objects.all()
    return render(request,'bankList.html',{'mydata':data})

class UpdateBank(View):
    def get(self,request,id):
        obj=get_object_or_404(Bloodbank,bloodbankid=id)
        myform=BloodbankForm(instance=obj)
        return render(request,'updBank.html',{'myform':myform})
    def post(self,request,id):
        obj=get_object_or_404(Bloodbank,bloodbankid=id)
        myform=BloodbankForm(request.POST,instance=obj)
        if myform.is_valid():
            myform.save()
            return redirect('bankList')

class DeleteBank(View):
    def get(self,request,id):
        obj=get_object_or_404(Bloodbank,bloodbankid=id)
        myform=BloodbankForm(instance=obj)
        return render(request,'delBank.html',{'myform':myform})
    def post(self,request,id):
        obj=get_object_or_404(Bloodbank,bloodbankid=id)
        obj.delete()
        return redirect('bankList')        
    
class AddDonor(View):
    def get(self,request):
        username=request.session['username']
        creator=request.session['created_by']
        bbnm=Bloodbank.objects.get(username=creator)
        myform=DonorForm()
        return render(request,'addDonor.html',{'myform':myform,'username':username,'bbnm':bbnm})        
    def post(self,request):
        username=request.session['username']
        creator=request.session['created_by']
        bbnm=Bloodbank.objects.get(username=creator)
        myform=DonorForm(request.POST)
        if myform.is_valid():
            donorid=myform.cleaned_data['donorid']
            dname=myform.cleaned_data['dname']
            address=myform.cleaned_data['address']
            city=myform.cleaned_data['city']
            contact=myform.cleaned_data['contact']
            bloodgroup=myform.cleaned_data['bloodgroup']
            qty=myform.cleaned_data['qty']
            bloodbagno=myform.cleaned_data['bloodbagno']
            bloodCollectiondt=myform.cleaned_data['bloodCollectiondt']
            bloodExpirydt=myform.cleaned_data['bloodExpirydt']
            bloodbankid=bbnm.bloodbankid
            status=myform.cleaned_data['status']
            username=username
            p=Donor(donorid,dname,address,city,contact,bloodgroup,qty,bloodbagno,bloodCollectiondt,bloodExpirydt,bloodbankid,status,username)
            p.save()
            # myform.save()
            return redirect('home')
        else:
            return HttpResponse("<h5>Data could not be added...")

class UpdateDonor(View):
    def get(self,request,id):
        obj=get_object_or_404(Donor,donorid=id)
        myform=DonorForm(instance=obj)
        return render(request,'updDonor.html',{'myform':myform})
    def post(self,request,id):
        obj=get_object_or_404(Donor,donorid=id)
        myform=DonorForm(request.POST,instance=obj)
        if myform.is_valid():
            myform.save()
            return redirect('donorList')

class DeleteDonor(View):
    def get(self,request,id):
        obj=get_object_or_404(Donor,donorid=id)
        myform=DonorForm(instance=obj)
        return render(request,'delDonor.html',{'myform':myform})
    def post(self,request,id):
        obj=get_object_or_404(Donor,donorid=id)
        obj.delete()
        return redirect('donorList') 

def donorList(request):
    username=request.session['username']
    data=Bloodbank.objects.get(username_id=username)
    data=Donor.objects.filter(bloodbankid=data.bloodbankid)
    return render(request,'donorList.html',{'mydata':data})

class AddReceiver(View):
    def get(self,request):
        username=request.session['username']
        creator=request.session['created_by']
        bbnm=Bloodbank.objects.get(username=creator)
        myform=ReceiverForm()
        return render(request,'addReceiver.html',{'myform':myform,'username':username,'bbnm':bbnm})        

    def post(self,request):
        myform=ReceiverForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('home')
        else:
            return HttpResponse("<h5>Data could not be added...")          

class UpdateReceiver(View):
    def get(self,request,id):
        obj=get_object_or_404(Receiver,receiverid=id)
        myform=ReceiverForm(instance=obj)
        return render(request,'updReceiver.html',{'myform':myform})
    def post(self,request,id):
        obj=get_object_or_404(Receiver,receiverid=id)
        myform=ReceiverForm(request.POST,instance=obj)
        if myform.is_valid():
            myform.save()
            return redirect('receiverList')

class DeleteReceiver(View):
    def get(self,request,id):
        obj=get_object_or_404(Receiver,receiverid=id)
        myform=ReceiverForm(instance=obj)
        return render(request,'delReceiver.html',{'myform':myform})
    def post(self,request,id):
        obj=get_object_or_404(Receiver,receiverid=id)
        obj.delete()
        return redirect('receiverList') 

def receiverList(request):
    data=Receiver.objects.all()
    return render(request,'receiverList.html',{'mydata':data})

class SearchDonor(View):
    def get(self,request):
        return render(request,'search.html')
    def post(self,request):
        bg=request.POST['bg']
        ct=request.POST.get('ct')
        if(bg and not ct):
            data=Donor.objects.filter(bloodgroup__iexact=bg)
        elif(ct and not bg):
            data=Donor.objects.filter(city__iexact=ct)
        elif(bg and ct):
            data=Donor.objects.filter(bloodgroup__iexact=bg).filter(city__iexact=ct)
        else:
            data=Donor.objects.all()
        return render(request,'donordata.html',{'mydata':data})


class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        unm=request.POST['unm']
        pwd=request.POST['pass']
        userdata=MyUser.objects.filter(username__exact=unm).filter(password__exact=pwd)
        if userdata:
            for user in userdata:
                request.session['utype']=user.usertype
                request.session['uname']=user.firstname+" "+user.lastname
                request.session['username']=user.username
                request.session['created_by']=user.created_by
            return redirect('home')
        else:
            return HttpResponse("<h3>Invalid User Details....</h3>")
        

class Registration(View):
    def get(self,request):
        creator=request.session['username']
        myform=UserForm()
        return render(request,'register.html',{'myform':myform,'creator':creator})
    def post(self,request):
        myform=UserForm(request.POST)
        creator=request.session['username']
        if myform.is_valid():
            username=myform.cleaned_data['username']
            firstname=myform.cleaned_data['firstname']
            lastname=myform.cleaned_data['lastname']
            password=myform.cleaned_data['password']
            usertype=myform.cleaned_data['usertype']
            created_by=creator
            p=MyUser(username,firstname,lastname,password,usertype,created_by)
            p.save()
            # myform.save()
        return redirect('logins')

def logouts(request):
        logout(request)
        return redirect('home')


class UpdateProfile(View):
    def get(self,request):
        username=request.session['username']
        utype=request.session['utype']
        if(utype=='bloodbank'):
            data=Bloodbank.objects.get(username_id=username)
            obj=get_object_or_404(Bloodbank,bloodbankid=data.bloodbankid)
            myform=BloodbankForm(instance=obj)
        elif(utype=='donor'):
            data=Donor.objects.get(username_id=username)
            obj=get_object_or_404(Donor,donorid=data.donorid)
            myform=DonorForm(instance=obj)
        elif(utype=='receiver'):
            data=Receiver.objects.get(username_id=username)
            obj=get_object_or_404(Receiver,receiverid=data.receiverid)
            myform=ReceiverForm(instance=obj)
        return render(request,'updateProfile.html',{'myform':myform})
    def post(self,request):
        username=request.session['username']
        utype=request.session['utype']
        if(utype=='bloodbank'):
            data=Bloodbank.objects.get(username_id=username)
            obj=get_object_or_404(Bloodbank,bloodbankid=data.bloodbankid)
            myform=BloodbankForm(request.POST,instance=obj)
        elif(utype=='donor'):
            data=Donor.objects.get(username_id=username)
            obj=get_object_or_404(Donor,donorid=data.donorid)
            myform=DonorForm(request.POST,instance=obj)
        elif(utype=='receiver'):
            data=Receiver.objects.get(username_id=username)
            obj=get_object_or_404(Receiver,receiverid=data.receiverid)
            myform=ReceiverForm(request.POST,instance=obj)

        if myform.is_valid():
            myform.save()
            return redirect('home')