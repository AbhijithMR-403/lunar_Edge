from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from user_cart.models import Coupon
from authenticator.models import Account
from product_management.models import Product, Product_Variant
from admin_panel.form import Coupon_form
from order.models import Order

# ^ Template Path
chart_path = "admin_partition/chart/"


# ^ Dashboard
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('admin_panel:login')

    total_users_count = int(Account.objects.count())
    product_count = Product.objects.count()
    user_order = Order.objects.count()
    completed_orders = Order.objects.filter()
    monthly_totals_dict = defaultdict(float)

    for order in completed_orders:
        order_month = order.created_at.strftime('%m-%Y')
        monthly_totals_dict[order_month] += float(order.order_total)

    print(monthly_totals_dict)
    months = list(monthly_totals_dict.keys())
    totals = list(monthly_totals_dict.values())

    variants = Product_Variant.objects.all()

    context = {
        'total_users_count': total_users_count,
        'product_count': product_count,
        'order': user_order,
        'variants': variants,
        'months': months,
        'totals': totals,
    }
    return render(request, f'{chart_path}admin_chart.html', context)


# ^ Logout
def logout_admin(request):
    logout(request)
    return redirect('admin_panel:login')


#  ^ admin login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    logout(request)
    print(request.user, '\n\n\n\n')
    if request.user.is_superuser:
        print('\n\nsdfadfa\n\n\n')
        redirect('admin_panel:dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            if not Account.objects.filter(email=email).exists():
                messages.warning(request, 'No user found')
                return redirect('admin_panel:login')
        except:
            pass
        # only needed when you are doing email validation

        user = authenticate(email=email, password=password)
        if user is None:
            messages.warning(request, 'Invalid detailes')
            return redirect('admin_panel:login')
        else:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_panel:dashboard')
            else:
                messages.warning(request, 'Only for superuser')

    return render(request, 'admin_partition/sign_in/login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_list(request):
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    user_details = Account.objects.all().filter(is_superuser=False)
    content = {
        'user_details': user_details
    }
    return render(request, 'admin_partition/user_list.html', content)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_unblock_user(request, id, block):
    if not request.user.is_superuser:
        return redirect('admin_panel:login')

    try:
        user = Account.objects.get(id=id)
        user.is_active = (block == 1)
        user.save()
    except Exception:
        messages.warning('There is no such user')
        pass
    return redirect('admin_panel:user_list')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def coupon(request):
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    form = Coupon_form
    if request.method == "POST":
        form = Coupon_form(request.POST)
        if not form.is_valid():
            return render(request, 'admin_partition/addproduct.html',
                          {'form': form})
        form.save()
        return redirect('product:add_product')
    return render(request, 'admin_partition/addfield.html', {'form': form})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def chart(request):
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    total_users_count = int(Account.objects.count())
    product_count = Product.objects.count()
    order = Order.objects.filter().count()
    completed_orders = Order.objects.filter()

    monthly_totals_dict = defaultdict(float)

    # Iterate over completed orders and calculate monthly totals
    for order in completed_orders:
        order_month = order.created_at.strftime('%m-%Y')
        monthly_totals_dict[order_month] += float(order.order_total)
    months = list(monthly_totals_dict.keys())
    totals = list(monthly_totals_dict.values())
    variants = Product_Variant.objects.all()

    context = {
        'total_users_count': total_users_count,
        'product_count': product_count,
        'order': order,
        'variants': variants,
        'months': months,
        'totals': totals,
    }
    return render(request, f'{chart_path}admin_chart.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def report(request):
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    sales = Order.objects.select_related('user', 'shipping_address', 'payment').all()

    p = Paginator(sales, 5)
    page = request.GET.get('page')
    try:
        sales_page = p.get_page(page)
    except PageNotAnInteger:
        sales_page = p.page(1)
    except EmptyPage:
        sales_page = p.page(p.num_pages)

    context = {
        'sales': sales_page,
    }
    return render(request, f'{chart_path}report.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def filtered_sales(request):
    if not request.user.is_superuser:
        return redirect('admin_panel:login')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    from_date = f'{start_date}+00:00'
    to_date = f'{end_date} 23:59:59+00:00'
    orders = Order.objects.filter(
        created_at__gte=from_date, created_at__lte=to_date)

    context = {
        "sales": orders,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, f'{chart_path}report.html', context)
