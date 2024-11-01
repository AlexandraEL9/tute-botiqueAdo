from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.

# view bag
def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')

# add to bag
def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('product_size', None)
    bag = request.session.get('bag', {})

    # Ensure bag[item_id] is always a dictionary structure
    if item_id not in bag:
        bag[item_id] = {'items_by_size': {}, 'quantity': 0}

    if size:
        # Handle items with sizes
        if size in bag[item_id]['items_by_size']:
            bag[item_id]['items_by_size'][size] += quantity
        else:
            bag[item_id]['items_by_size'][size] = quantity
    else:
        # Handle items without sizes
        bag[item_id]['quantity'] += quantity

    # Update the session
    request.session['bag'] = bag
    return redirect(redirect_url)

# update product quantities in the bag
def adjust_bag(request, item_id):
    """ Update the quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['item_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

# remove product from the bag
def remove_item_from_bag(request, item_id):
    """ Remove an item from the shopping bag """
    try:

        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['item_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)