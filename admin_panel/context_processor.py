

def nav_bar(request):
    url = request.build_absolute_uri()
    print(url[-15:])
    activate_bar = 1
    if 'dashboard' in url:
        activate_bar = 1
    if 'product_list' in url:
        activate_bar = 2
    if 'order_list' in url or 'coupon' in url:
        activate_bar = 3
    if 'category_list' in url:
        activate_bar = 4
    if 'user_list' in url:
        activate_bar = 5
    if 'report' in url:
        activate_bar = 6
    if 'add_product' in url or 'attribute' in url or 'brand' in url:
        print('wooo')
        activate_bar = 7
    print(activate_bar)
    context = {
        "current_tag": activate_bar,
    }
    print(context)
    return context