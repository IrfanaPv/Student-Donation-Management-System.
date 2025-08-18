from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import Student,CoustomUser,Donation,Donation_request,Donor
from django.contrib import messages
from django.db.models import Q,Sum
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template import Context
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


# Create your views here.
def home_page(request):
    return render(request,'homepage.html')
def login_page(request):
    return render(request,'login_page.html')
def login_save(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        User=authenticate(request,username=username,password=password)
        if User is not None:
            login(request,User)
            messages.success(request, 'Logined Successfully!')
            if User.is_superuser:
                return redirect(admin_dashboard)
            if User.is_student:
                return redirect(student_dashboard)
            if User.is_doner:
                return redirect(donor_dashboard)
        else:
            messages.error(request, "Invalid username or password!")
            return render(request,'login_page.html')

def help_request(request):
    data=Student.objects.all()    
    return render(request,'help_request.html',{'data':data})
def save_request(request):
    if request.method=="POST":
        stud_id=request.POST['stud_id']
        cat=request.POST['category']
        sd=request.POST['description']
        sid=request.POST['id_doc']
        si=request.POST['income_doc']
        sa=request.POST['amount']
        x=Donation_request.objects.create(stud_id=stud_id,catogery=cat,description=sd,id_document=sid,income_certificate=si,amount_needed=sa)
        x.save()
        messages.success(request, "Request Submitted successfully!")
        return render(request, 'help_request.html')
def register_student(request):
    return render(request,'register_student.html')
def save_student(request):
        if request.method=="POST":
             un=request.POST['username']
             sn=request.POST['sname']
             sa=request.POST['sage']
             se=request.POST['semail']
             sc=request.POST['cnumber']
             sad=request.POST['saddress']
             sp=request.POST['password']
             data=CoustomUser.objects.create_user(username=un,password=sp,is_student=True)
             a=Student.objects.create(name=sn,age=sa,contact_number=sc,address=sad,user=data,email=se)
             a.save()
             messages.success(request, "Registered successfully!")
             return render(request, 'register_student.html')
def student_dashboard(request):
     logined_user=request.user
     username=request.user.username
     data=Student.objects.get(user=logined_user)
     x=Donation_request.objects.filter(stud=data)
     return render(request,'student_dashboard.html',{'username':username,'data':data,'x':x})
def register_donor(request):
    return render(request,'register_donor.html')
def save_donor(request):
        if request.method=="POST":
             un=request.POST['uname']
             dn=request.POST['dname']
             de=request.POST['demail']
             dc=request.POST['cnumber']
             dad=request.POST['daddress']
             dp=request.POST['dpass']
             data=CoustomUser.objects.create_user(username=un,password=dp,is_doner=True)
             a=Donor.objects.create(name=dn,contact_number=dc,address=dad,user=data,email=de)
             a.save()
             messages.success(request, "Registered successfully!")
             return render(request, 'register_donor.html')
     

def donation(request):
    category = request.GET.get('category')
    max_amount = request.GET.get('max_amount')
    location = request.GET.get('location')

    requests = Donation_request.objects.all()

    if category:
        requests = requests.filter(catogery=category)

    if max_amount:
        requests = requests.filter(amount_needed__lte=max_amount)

    if location:
        requests = requests.filter(location__icontains=location)

    return render(request, 'donation.html', {'requests':requests})


def donor_dashboard(request):
    logined_user=request.user
    username=request.user.username
    data=Donor.objects.get(user=logined_user)
    x=Donation.objects.all()
    total=sum(d.amount for d in x)
    return render(request,'donor_dashboard.html',{'username':username,'data':data,'x':x,'total':total})
def admin_dashboard(request):
    logined_user=request.user
    username=logined_user.username
    data=logined_user
    students=Student.objects.all()
    doner=Donor.objects.all()
    req=Donation_request.objects.all().order_by('-created_at')
    donations=Donation.objects.all()
    pending_req=Donation_request.objects.filter(status='pending')
    total_students=students.count()
    total_donors=doner.count()
    total_requests=req.count()
    total_donated=donations.count()
    total_pendingrequests=pending_req.count()
    return render(request,'admin_page.html',
                  {'username':username,
                   'data':data,
                   'req':req,
                   'students':students,
                   'doner':doner,
                   'donations':donations,
                   'total_students':total_students,
                   'total_donors':total_donors,
                   'total_requests':total_requests,
                   'total_donated':total_donated,
                   'total_pendingrequests':total_pendingrequests,
                   'pending_req':pending_req
                   })


def approve_request(request,id):
     r=Donation_request.objects.get(id=id)
     r.status='approved'
     r.save()
     messages.success(request, "Approved!")
     return redirect(view_requests)
def reject_request(request,id):
     r=Donation_request.objects.get(id=id)
     r.status='reject'
     r.save()
     messages.warning(request, "rejected!")
     return redirect(view_requests)
def view_donations(request):
     donations=Donation.objects.all()
     return render(request,'view_donations.html',{'donations':donations})
def view_requests(request):
       req=Donation_request.objects.all().order_by('-created_at')
       return render(request,'view_requests.html',{'req':req})
def view_sudents(request):
     students=Student.objects.all()
     return render(request,'view_students.html',{'students':students})
def view_donors(request):
     doner=Donor.objects.all()
     return render(request,'view_donors.html',{'doner':doner})
def view_pendingrequests(request):
     pending_req=Donation_request.objects.filter(status='pending')
     return render(request,'view_pendingrequests.html',{'pending_req':pending_req})




def download_report_pdf(request):
    students = Student.objects.all()
    donors = Donor.objects.all()
    donations = Donation.objects.all()
    donation_requests = Donation_request.objects.all()
    total_donationrequests=donation_requests.count()
    total_donation_amount = donations.aggregate(total=Sum('amount'))['total'] or 0


    template_path = 'admin_report_pdf.html'  # We will create this template
    context = {
        'students': students,
        'donors': donors,
        'donations': donations,
        'donation_requests': donation_requests,
        'total_donationrequests':total_donationrequests,
        'total_donation_amount':total_donation_amount

    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admin_report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def logout_page(request):
    logout(request)
    return redirect(home_page)
def student_profile(request):
     logined_user=request.user
     username=request.user.username
     p=Student.objects.get(user=logined_user)
     return render(request,'student_profile.html',{'p':p})
def update_student(request):
     logined_user=request.user
     username=request.user.username
     y=Student.objects.get(user=logined_user)
     return render(request,'edit_student.html',{'y':y})
def s_updation(request,id):
     if request.method=="POST":
        un=request.POST['username']
        sn=request.POST['sname']
        sa=request.POST['sage']
        se=request.POST['semail']
        sc=request.POST['cnumber']
        sad=request.POST['saddress']
        x=Student.objects.get(id=id)
        x.User=un
        x.name=sn
        x.age=sa
        x.email=se
        x.contact_number=sc
        x.address=sad
        x.save()
        return redirect(student_profile)
def donor_profile(request):
     logined_user=request.user
     username=request.user.username
     d=Donor.objects.get(user=logined_user)
     return render(request,'donor_profile.html',{'d':d})
def update_donor(request):
     logined_user=request.user
     username=request.user.username
     z=Donor.objects.get(user=logined_user)
     return render(request,'edit_donor.html',{'z':z})
def d_updation(request,id):
     if request.method=="POST":
        un=request.POST['username']
        dn=request.POST['dname']
        de=request.POST['demail']
        dc=request.POST['cnumber']
        dad=request.POST['daddress']
        d=Donor.objects.get(id=id)
        d.User=un
        d.name=dn
        d.email=de
        d.contact_number=dc
        d.address=dad
        d.save()
        return redirect(donor_profile)



def create_order(request, req_id):
    donation_req = get_object_or_404(Donation_request, id=req_id)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    amount_paise = int(donation_req.amount_needed * 100) 


    order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "order": order,
        "donation_req": donation_req,
        "razorpay_key": settings.RAZORPAY_KEY_ID
      
    }
    return render(request, "payment_page.html", context)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            req_id = request.POST.get("req_id")
            amount = request.POST.get("amount")
        
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            params_dict = {
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': razorpay_signature
            }

            client.utility.verify_payment_signature(params_dict)

            donor = Donor.objects.get(user=request.user)
            donation_req = Donation_request.objects.get(id=req_id)

            Donation.objects.create(
            donor=donor,
            donation_request=donation_req,
            amount=amount
            )
            return render(request, "payment_success.html")
        except razorpay.errors.SignatureVerificationError:
            return render(request, "payment_failed.html")
    return render(request, 'payment_failed.html')
