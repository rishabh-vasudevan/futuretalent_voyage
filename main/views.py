from django.shortcuts import render, redirect
from Accounts.models import UserAccount
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .models import Room,Booking,Comment
from datetime import datetime
from Voyage.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def Description(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        room = Room.objects.get(room_id=id)
        comments = Comment.objects.filter(room_id=id)
        param = {'object' : room, 'object1' : comments}
    return render(request,'main/description.html',param)

def Home(request):
    instance = Room.objects.filter(verified = True)
    instance = instance[0:4]
    param = {'objects': instance}
    return render(request,'main/home.html',param)

def Register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact = request.POST.get('contact')
        name = request.POST.get('name')
        user = UserAccount.objects.create_user(username=name, email = email, password = password, contact_no = contact)
        user = authenticate(email=email, password=password)
        if user is not None:
            return redirect('/')
        return render(request, '/',)

def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login')
    return render(request, 'main/login.html')

def Room_List(request):
    if request.method == 'POST':
        arrive = request.POST.get('arrive')
        departure = request.POST.get('departure')
        adults = request.POST.get('adults')

        arrive = datetime.date(datetime.strptime(arrive, '%Y-%m-%d'))
        departure = datetime.date(datetime.strptime(departure, '%Y-%m-%d'))
    
        instance = Room.objects.all()
        bookings = Booking.objects.all()
        param = {'objects': []}
        rooms = []
        for i in bookings.iterator():
            if i.start >= departure or i.end <= arrive:
                id = i.room_id
                if id not in rooms:
                    rooms.append(id)
                    param['objects'].append(Room.objects.get(room_id=id))
        for i in instance.iterator():
            flag=0
            for j in bookings.iterator():
                if i.room_id ==j.room_id:
                    flag=1
            if flag == 0:
                param['objects'].append(Room.objects.get(room_id=i.room_id))


        return render(request, 'main/room_list.html', param)
    else:
        instance = Room.objects.filter(verified = True)
        param = {'objects': instance}
        return render(request, 'main/room_list.html', param)

@login_required(login_url='/login')



def Adminpage(request):
    verified_rooms = Room.objects.filter(verified = False)
    rooms = []
    for i in verified_rooms:
        if i.rejected == False:
            rooms.append(i)
    param = {'objects':rooms}
    return render(request,'main/landlord.html',param)

def Comments(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        comment = request.POST.get('comment')
        Comment.objects.create(room_id = id, comment = comment, user = request.user)
        return redirect('/description?id='+id)

def Book(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        arrive = request.GET.get('arrive')
        departure = request.GET.get('departure')
        adults = request.GET.get('adults')
        arrive1 = arrive
        departure1 = departure
        arrive = datetime.date(datetime.strptime(arrive, '%Y-%m-%d'))
        departure = datetime.date(datetime.strptime(departure, '%Y-%m-%d'))

        instance = Room.objects.all()
        bookings = Booking.objects.filter(room_id = id)
        flag = 1
        for i in bookings.iterator():
            if not(i.start >= departure or i.end <= arrive):
                flag = 0
        if flag == 1:
            room = Room.objects.get(room_id = id)
            param = {'object' : room, 'start' : arrive1, 'end': departure1, 'adults': adults }
            return render(request,'main/book.html',param)
    return render(request,'main/book.html')

def Payment(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        arrive = request.GET.get('start')
        departure = request.GET.get('end')
        adults = request.GET.get('adults')
        Booking.objects.create(user = request.user , start = arrive, end = departure, room_id = id , adults = adults)

        subject = 'Voyage Booking Confirmation'
        message = f'{request.user.username} your booking from the dates {arrive} to {departure} for {adults} Adults has been confirmed'

        send_mail(subject, 
                  message, 
                  EMAIL_HOST_USER, 
                  [request.user.email], 
                  fail_silently = False)    
    
    return redirect('/')

def Logout(request):
    logout(request)
    return redirect('/')

def Advertise(request):
    if request.method == 'POST':
        if not request.POST['id']:
            if request.user.is_landlord:
                instance = Room(
                    user = request.user,
                    price=request.POST['price'], 
                    details=request.POST['details'],
                    room_desc=request.POST['room_desc'], 
                    address=request.POST['address'], 
                    cover_image=request.FILES['cover_image'],
                    image_1=request.FILES['image_1'],
                    )

                for i in range(2, 11):
                    tmp = f'image_{i}'
                    try:
                        instance.tmp = request.FILES[tmp]
                    except:
                        pass
                instance.save()
                
                return redirect('/')
            else:
                return HttpResponse("User is not a LandLord") 
        else:
            if request.user.is_landlord:
                id = request.POST.get('id')
                try:
                    room = Room.objects.get(room_id = id)
                    room.delete()
                except:
                    pass
                instance = Room(
                    user = request.user,
                    price=request.POST['price'], 
                    details=request.POST['details'],
                    room_desc=request.POST['room_desc'], 
                    address=request.POST['address'], 
                    cover_image=request.FILES['cover_image'],
                    image_1=request.FILES['image_1'],
                    )

                for i in range(2, 11):
                    tmp = f'image_{i}'
                    try:
                        instance.tmp = request.FILES[tmp]
                    except:
                        pass
                instance.save()
                
                return redirect('/')
            else:
                return HttpResponse("User is not a LandLord")
    return render(request, 'main/advertise.html')

def VerifyRoom(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        reason = request.POST.get('reason')
        room = Room.objects.get(room_id = id)
        room.rejected = True
        room.save()

        user = UserAccount.objects.get(username = room.user)
        subject = 'Advertisement Rejected'
        message = f'{request.user.username} your advertisement has been requested because {reason}'

        send_mail(subject, 
                  message, 
                  EMAIL_HOST_USER, 
                  [user.email], 
                  fail_silently = False)

        return redirect('/adminpage')
    else:
        room = Room.objects.get(room_id = int(request.GET.get('id')))
        room.verified = True
        room.save()
        return redirect('/adminpage')
