from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm
from .models import FoodProcess   
from .models import FoodItem
from .forms import FoodItemForm 
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings 
# payments 
from .models import Order, OrderItem, FoodItem
import razorpay 
from django.views.decorators.csrf import csrf_exempt

# for message for LOgin and register page 
from django.contrib import messages


def is_staff_user(user):
    return user.is_authenticated and user.is_staff

def home(request):
    processes = FoodProcess.objects.all()
    food_items = FoodItem.objects.all()
    return render(request, 'home.html', {
        'processes': processes,
        'food_items': food_items
    })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Registration successful! Please login.")
            return redirect('login')
        else:
            messages.error(request, "⚠️ Registration failed. Please check the form and try again.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"🎉 Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "❌ Invalid username or password.")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "👋 You have been logged out.")
    return redirect('home')


@user_passes_test(is_staff_user)
def staff_dashboard(request):
    items = FoodProcess.objects.all()
    return render(request, 'staff_dashboard.html', {'items': items})

from django.contrib.auth.decorators import login_required

@login_required
def guest_page(request):
    items = FoodProcess.objects.all()
    return render(request, 'guest_page.html', {'items': items})

# Check staff function
def staff_check(user):
    return user.is_staff

@login_required
@user_passes_test(staff_check)
def staff_dashboard(request):
    return render(request, "staff_dashboard.html")

@login_required
@user_passes_test(staff_check)
def add_item(request):
    return render(request, "add_item.html")

@login_required
@user_passes_test(staff_check)
def manage_items(request):
    return render(request, "manage_items.html") 

# Staff check
def staff_required(user):
    return user.is_authenticated and user.is_staff

# Add item
@login_required
@user_passes_test(staff_required)
def add_item(request):
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item added successfully ✅")
            return redirect('manage_items')
        else:
            messages.error(request, "Error adding food ❌")
    else:
        form = FoodItemForm()
    return render(request, "add_item.html", {"form": form})

# Manage items
@login_required
@user_passes_test(staff_required)
def manage_items(request):
    items = FoodItem.objects.all()
    return render(request, "manage_items.html", {"items": items})

# Edit item
@login_required
@user_passes_test(staff_required)
def edit_item(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item updated successfully ✅")
            return redirect('manage_items')
        else:
            messages.error(request, "Error updating food ❌")
    else:
        form = FoodItemForm(instance=item)
    return render(request, "add_item.html", {"form": form, "edit": True})

# Delete item
@login_required
@user_passes_test(staff_required)
def delete_item(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id)
    item.delete()
    messages.success(request, "Food item deleted ✅")
    return redirect('manage_items')


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # ✅ Send Email
            subject = f"📩 New Contact Message from {contact.name}"
            message = f"""
            You received a new message from your website:

            Name: {contact.name}
            Email: {contact.email}

            Message:
            {contact.message}
            """

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,  # from email
                    ["amir.my2004@gmail.com"],      # to email (can be multiple)
                    fail_silently=False,
                )
                messages.success(request, "✅ Your message has been sent successfully!")
            except Exception as e:
                messages.error(request, f"❌ Message saved but email not sent: {e}")

            return redirect('contact')
        else:
            messages.error(request, "❌ Error sending message. Please check the form.")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form}) 

    # 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 



client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)) 

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id)
    order, created = Order.objects.get_or_create(user=request.user, status="Pending")
    order_item, created = OrderItem.objects.get_or_create(order=order, food_item=item)

    if not created:
        order_item.quantity += 1
    order_item.save()

    # Recalculate total
    order.total_amount = sum(i.price for i in order.items.all())
    order.save()

    messages.success(request, f"Added {item.name} to your cart ✅")
    return redirect("view_cart")


@login_required
def remove_from_cart(request, item_id):
    order = Order.objects.filter(user=request.user, status="Pending").first()
    if order:
        order_item = get_object_or_404(OrderItem, order=order, food_item_id=item_id)
        order_item.delete()

        # Recalculate total
        order.total_amount = sum(i.price for i in order.items.all())
        order.save()

        messages.success(request, "Item removed from cart ❌")
    return redirect("view_cart")


@login_required
def decrease_quantity(request, item_id):
    order = Order.objects.filter(user=request.user, status="Pending").first()
    if order:
        order_item = get_object_or_404(OrderItem, order=order, food_item_id=item_id)
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order_item.delete()

        # Recalculate total
        order.total_amount = sum(i.price for i in order.items.all())
        order.save()

        messages.info(request, "Quantity updated 📝")
    return redirect("view_cart")

@login_required
def view_cart(request):
    order = Order.objects.filter(user=request.user, status="Pending").first()
    print("DEBUG ORDER:", order)
    if order:
        print("DEBUG ITEMS:", order.items.all())
    return render(request, "cart.html", {"order": order})



@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, status="Pending").first()
    if not order or not order.items.exists():
        messages.error(request, "Your cart is empty ❌")
        return redirect("view_cart") 

    import requests

    try:
        test = requests.get("https://api.razorpay.com/v1/orders", auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        print("✅ Razorpay reachable:", test.status_code)
    except Exception as e:
        print("❌ Razorpay connection failed:", e)

    # Convert to paise (Razorpay requires amount in INR paise)
    amount = int(order.total_amount * 100)

    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    # Save Razorpay order id
    order.razorpay_order_id = razorpay_order["id"]
    order.save()

    context = {
        "order": order,
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "currency": "INR",
        "callback_url": request.build_absolute_uri("/payment/verify/"),
    }
    return render(request, "checkout.html", context) 



@csrf_exempt
def payment_verify(request):
    if request.method == "POST":
        try:
            params_dict = {
                "razorpay_order_id": request.POST.get("razorpay_order_id"),
                "razorpay_payment_id": request.POST.get("razorpay_payment_id"),
                "razorpay_signature": request.POST.get("razorpay_signature"),
            }

            print("🔎 Payment Data:", params_dict)

            # Ensure all 3 values exist
            if not all(params_dict.values()):
                messages.error(request, "❌ Payment verification failed (missing fields).")
                return redirect("view_cart")

            # Verify signature
            client.utility.verify_payment_signature(params_dict)

            # Mark order complete
            order = Order.objects.get(razorpay_order_id=params_dict["razorpay_order_id"])
            order.payment_completed = True
            order.status = "Preparing"
            order.save()

            messages.success(request, f"✅ Payment successful! Order #{order.id} placed.")
            return redirect("home")

        except razorpay.errors.SignatureVerificationError as e:
            print("❌ Razorpay Signature Error:", e)
            messages.error(request, "❌ Payment verification failed (invalid signature).")
            return redirect("view_cart")

        except Exception as e:
            print("❌ Unexpected error:", e)
            messages.error(request, "❌ Payment verification failed due to server error.")
            return redirect("view_cart")
    return redirect("home")
