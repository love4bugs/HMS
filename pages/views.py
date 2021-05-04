from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect!')
    context = {}
    return render(request, 'login.html', context)

def room_detail(request, my_pk):
    obj = Room.objects.get(pk = my_pk)
    content =  {
        "instance": obj
    }
    return render(request, 'room.html', content)

def home_view(request, *args, **kwargs):
    return render(request, 'home.html')

def room_create(request, *args, **kwargs):
    form = RoomForm()
    content =  {
        "form": form
    }

    if request.method == 'POST':
        form = RoomForm(request.POST)
       
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect('../home')

    return render(request, 'create.html', content)


def book_view(request, *args, **kwargs):
    form = BookingForm()
    queryset = Room.objects.filter(empty = True)
    content =  {
        "form": form,
        "qs": queryset
    }

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            Room.objects.filter(room_no = form.cleaned_data['room_no']).update(empty = False)
            form.save()
            return redirect('/home')
        else:
            content =  {
                "form": form,
                "qs": queryset
            }
    return render(request, 'booking.html', content)

def bill_view(request):
    form = CheckoutForm()
    queryset = Room.objects.filter(empty = False)
    content =  {
        "form": form,
        "qs": queryset
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            instance = form.save()
            Checkout.objects.filter(pk=instance.pk).update(
                                        consumer = Costumer.objects.filter(room_no = instance.room_no, phone = instance.phone, active = True)[0])
            return redirect(str(int(form.cleaned_data['phone']))+'/')
        else:
            content =  {
                "form": form,
                "qs": queryset
            }
        
    return render(request, 'billing.html', content)


def resturant_bill(request):
    queryset = Item.objects.all()
    content = {
        'qs': queryset
    }
    if request.method == 'POST':
        room_id = request.POST.get("room_no")
        if room_id:
            try:
                obj_consumer = Costumer.objects.filter(room_no = int(room_id), active = True)[0]
            except Exception:
                messages.info(request, 'Invalid Room Number! or Room is Empty!')
                return render(request, 'resturant_bill.html', content)
        else:
            obj_consumer = None
        order_id = datetime.timestamp(datetime.now())

        empty_flag = True
        for i in queryset:
            quant = request.POST.get(str(i.item_id))
            if quant:
                empty_flag = False
                obj_item = Item.objects.get(item_id =int(i.item_id))
                RestaurantParchase.objects.create(
                                                    consumer = obj_consumer,
                                                    item = obj_item,
                                                    qunatity = int(quant),
                                                    order_id = order_id
                                                )
        if empty_flag:
            messages.info(request, 'Invalid Order!')
        else:
            return redirect(str(int(order_id))+'/')
    return render(request, 'resturant_bill.html', content)

def resturant_reciept(request, my_order,*args, **kwargs):
    query_set = RestaurantParchase.objects.filter(order_id = my_order)
    item_list = []
    total = 0
    for instance in query_set:
        item_list.append({
                            'name': instance.item.item_name, 
                            'qunatity':instance.qunatity, 
                            'cost': instance.item.item_cost*instance.qunatity
                        })
        total += instance.item.item_cost*instance.qunatity
    
    if query_set[0].consumer != None and (query_set[0].consumer.package == 'P' or query_set[0].consumer.package == 'G'):
        total = 0
    content = {
                    'bill': item_list, 
                    'total': total, 
                    'tax': total*0.2,
                    'payable': total+total*0.2
                }
    return render(request, 'receipt.html', content)


def gym_bill(request):
    obj_gym = Gym.objects.first()
    content = {
        'obj': obj_gym
    }

    if request.method == 'POST':
        room_id = request.POST.get("room_no")
        if room_id:
            try:
                obj_consumer = Costumer.objects.filter(room_no = int(room_id), active = True)[0]
            except Exception:
                messages.info(request, 'Invalid Room Number! or Room is Empty!')
                return render(request, 'gym_bill.html', content)
        else:
            obj_consumer = None
        usage_id = datetime.timestamp(datetime.now())

        empty_flag = True
        time_spent = request.POST.get('time-spent')
        if time_spent:
            empty_flag = False
            GymUsage.objects.create(
                                        consumer = obj_consumer,
                                        gym = obj_gym,
                                        time_spent_in_hours = int(time_spent),
                                        usage_id = usage_id
                                    )
        if empty_flag:
            messages.info(request, 'Invalid Order!')
        else:
            return redirect(str(int(usage_id))+'/')
    return render(request, 'gym_bill.html', content)

def gym_reciept(request, my_usage_id,*args, **kwargs):
    obj = GymUsage.objects.get(usage_id = my_usage_id)
    total = obj.time_spent_in_hours * obj.gym.cost_per_hour
    if obj.consumer != None and obj.consumer.package == 'P':
        total = 0
    content = {
                    'cost': obj.gym.cost_per_hour, 
                    'time_spent': obj.time_spent_in_hours, 
                    'total': total,
                    'tax': total*0.2,
                    'payable': total+total*0.2
                }
    return render(request, 'gym_receipt.html', content)


def pool_bill(request):
    obj_pool = Pool.objects.first()
    content = {
        'obj': obj_pool
    }
    if request.method == 'POST':
        room_id = request.POST.get("room_no")
        if room_id:
            try:
                obj_consumer = Costumer.objects.filter(room_no = int(room_id), active = True)[0]
            except Exception:
                messages.info(request, 'Invalid Room Number! or Room is Empty!')
                return render(request, 'pool_bill.html', content)
        else:
            obj_consumer = None
        usage_id = datetime.timestamp(datetime.now())

        empty_flag = True
        time_spent = request.POST.get('time-spent')
        if time_spent:
            empty_flag = False
            PoolUsage.objects.create(
                                        consumer = obj_consumer,
                                        pool = obj_pool,
                                        time_spent_in_hours = int(time_spent),
                                        usage_id = usage_id
                                    )
        if empty_flag:
            messages.info(request, 'Invalid Order!')
        else:
            return redirect(str(int(usage_id))+'/')
    return render(request, 'pool_bill.html', content)

def pool_reciept(request, my_usage_id,*args, **kwargs):
    obj = PoolUsage.objects.get(usage_id = my_usage_id)
    total = obj.time_spent_in_hours * obj.pool.cost_per_hour
    if obj.consumer != None and obj.consumer.package == 'P':
        total = 0
    content = {
                    'cost': obj.pool.cost_per_hour, 
                    'time_spent': obj.time_spent_in_hours, 
                    'total': total,
                    'tax': total*0.2,
                    'payable': total+total*0.2
                }
    return render(request, 'pool_receipt.html', content)


def checkout_bill(request, my_phone,*args, **kwargs):
    obj = Checkout.objects.filter(phone=my_phone, paid=False)[0]
    obj1 = Costumer.objects.filter(phone=my_phone, active=True)[0]
    obj2 = Room.objects.get(room_no = obj.room_no)

    query_set = RestaurantParchase.objects.filter(consumer = obj1, paid = False).order_by('order_id')
    resturant_obj = []
    try:
        prev = query_set[0].order_id
        order = [datetime.fromtimestamp(prev)]
    except Exception:
        order = []
        pass
    for instance in query_set:
        if instance.order_id != prev:
            resturant_obj.append(order)
            prev = instance.order_id
            order = [datetime.fromtimestamp(prev)]
        order.append(instance)
    resturant_obj.append(order)
    resturant_cost = sum([obj.qunatity * obj.item.item_cost for obj in query_set])

    query_set1 = GymUsage.objects.filter(consumer = obj1, paid = False).order_by('usage_id')
    gym_obj = []
    try:
        prev = query_set1[0].usage_id
        order = [datetime.fromtimestamp(prev)]
    except Exception:
        pass
    for instance in query_set1:
        if instance.usage_id != prev:
            gym_obj.append(order)
            prev = instance.usage_id
            order = [datetime.fromtimestamp(prev)]
        order.append(instance)
    gym_obj.append(order)
    gym_cost = sum( [ obj.time_spent_in_hours * obj.gym.cost_per_hour for obj in query_set1 ] )

    query_set2 = PoolUsage.objects.filter(consumer = obj1, paid = False).order_by('usage_id')
    pool_obj = []
    try:
        prev = query_set2[0].usage_id
        order = [datetime.fromtimestamp(prev)]
    except Exception:
        pass
    for instance in query_set2:
        if instance.usage_id != prev:
            pool_obj.append(order)
            prev = instance.usage_id
            order = [datetime.fromtimestamp(prev)]
        order.append(instance)
    pool_obj.append(order)
    pool_cost = sum( [ obj.time_spent_in_hours * obj.pool.cost_per_hour for obj in query_set2 ] )

    if obj1.package == 'P':
        pool_cost = 0
        gym_cost = 0
        resturant_cost = 0
    elif obj1.package == 'G':
        resturant_cost = 0

    time = obj.checkout_time - obj1.checkin_time

    total = (time.days+1)*obj2.room_cost - obj1.advance + obj1.get_package_cost() + resturant_cost + gym_cost + pool_cost
    content = {
                'Name': obj.name,
                'Phone':my_phone,
                'Checkin': obj1.checkin_time,
                'Checkout': obj.checkout_time,
                'RoomNo': obj.room_no,
                'RoomCost': obj2.room_cost,
                'Duration': time.days+1,
                'Total_Room_Cost': (time.days+1)*obj2.room_cost - obj1.advance,
                'Advance': obj1.advance,
                'Package': obj1.get_package_name(),
                'PackageCost':obj1.get_package_cost(),
                'Resturant': resturant_obj,
                'Total_Resturant_Cost': resturant_cost,
                'Gym': gym_obj,
                'Total_Gym_Cost': gym_cost,
                'Pool': pool_obj,
                'Total_Pool_Cost': pool_cost,
                'total': total,
                'tax': total*0.2,
                'payable': total+total*0.2
            }
            
    Checkout.objects.filter(phone=my_phone).update(paid = True)
    Room.objects.filter(pk = obj2.pk).update(empty = True)
    RestaurantParchase.objects.filter(consumer = obj1).update(paid = True)
    GymUsage.objects.filter(consumer = obj1).update(paid = True)
    PoolUsage.objects.filter(consumer = obj1).update(paid = True)
    Costumer.objects.filter(pk = obj1.pk).update(active = False)

    return render(request, 'checkout.html', content)


def list_resturant_bills(request, *args, **kwargs):
    query_set = RestaurantParchase.objects.order_by('order_id')
    order_set = []
    total = 0

    try:
        prev = query_set[0].order_id
        obj = query_set[0].consumer
        if obj == None:
            obj = 'NA'
        order = [prev, obj]
        total += query_set[0].item.item_cost * query_set[0].qunatity
    except Exception:
        pass

    for index, instance in enumerate(query_set):
        if instance.order_id != prev:
            order.append(total)
            order_set.append(order)
            total = 0
            prev = instance.order_id
            obj = instance.consumer
            if obj == None:
                obj = 'NA'
            order = [prev, obj]
        if index != 0:
            total += instance.item.item_cost * instance.qunatity
    order.append(total)
    order_set.append(order)
    
    content = {
        'qs': order_set
    }

    return render(request, 'resturant_bills.html', content)