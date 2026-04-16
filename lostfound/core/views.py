from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count, Case, When, Value, IntegerField
from .models import Item, ClaimRequest, Notification
from .forms import ItemForm


# ✅ HOME PAGE WITH SEARCH & FILTER
def home(request):
    items = Item.objects.filter(is_resolved=False)
    
    # Advanced Search
    search_query = request.GET.get('q', '')
    item_type = request.GET.get('type', '')
    sort_by = request.GET.get('sort', 'latest')
    
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    if item_type:
        items = items.filter(item_type=item_type)

    if sort_by == 'oldest':
        items = items.order_by('id')
    elif sort_by == 'urgent':
        items = items.annotate(
            urgency_rank=Case(
                When(
                    Q(title__icontains='urgent') |
                    Q(description__icontains='urgent') |
                    Q(title__icontains='asap') |
                    Q(description__icontains='asap') |
                    Q(title__icontains='important') |
                    Q(description__icontains='important'),
                    then=Value(0)
                ),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by('urgency_rank', '-id')
    else:
        sort_by = 'latest'
        items = items.order_by('-id')
    
    context = {
        'items': items,
        'search_query': search_query,
        'item_type': item_type,
        'sort_by': sort_by,
    }
    return render(request, 'home.html', context)


# ✅ REGISTER
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('/')
    
    return render(request, 'register.html')


# ✅ LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


# ✅ LOGOUT
def logout_view(request):
    logout(request)
    return redirect('/')


# ✅ ADD ITEM
@login_required(login_url='login')
def add_item(request):
    form = ItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        messages.success(request, 'Item added successfully.')
        return redirect('/')
    return render(request, 'add_item.html', {'form': form})


# ✅ EDIT ITEM
@login_required(login_url='login')
def edit_item(request, id):
    item = get_object_or_404(Item, id=id)

    if item.user != request.user:
        return redirect('/')

    form = ItemForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'add_item.html', {'form': form, 'item': item})


# ✅ DELETE ITEM
@login_required(login_url='login')
def delete_item(request, id):
    item = get_object_or_404(Item, id=id)

    if item.user == request.user:
        item.delete()
        messages.success(request, 'Item deleted successfully.')
    else:
        messages.error(request, 'You are not allowed to delete this item.')

    return redirect('/')


# ✅ MARK ITEM AS RESOLVED
@login_required(login_url='login')
def resolve_item(request, id):
    item = get_object_or_404(Item, id=id)

    if item.user == request.user:
        item.is_resolved = True
        item.save()

    return redirect('/dashboard/')


# ✅ CLAIM ITEM
@login_required(login_url='login')
def claim_item(request, id):
    item = get_object_or_404(Item, id=id)

    if request.method == 'POST':
        ClaimRequest.objects.create(
            item=item,
            user=request.user,
            message=request.POST.get('message'),
            proof=request.FILES.get('proof')
        )

        Notification.objects.create(
            user=item.user,
            message=f"📬 {request.user.username} claimed your item: {item.title}",
            is_read=False
        )

        messages.success(request, 'Your claim has been submitted successfully.')

        return redirect('/')

    return render(request, 'claim.html', {'item': item})


# ✅ APPROVE CLAIM
@login_required(login_url='login')
def approve_claim(request, id):
    claim = get_object_or_404(ClaimRequest, id=id)

    if claim.item.user == request.user:
        claim.status = 'Approved'
        claim.save()
        
        # Notify claimer
        Notification.objects.create(
            user=claim.user,
            message=f"✅ Your claim for '{claim.item.title}' was approved!",
            is_read=False
        )
        messages.success(request, 'Claim approved successfully.')
    else:
        messages.error(request, 'You are not allowed to approve this claim.')

    return redirect('/dashboard/')


# ✅ REJECT CLAIM
@login_required(login_url='login')
def reject_claim(request, id):
    claim = get_object_or_404(ClaimRequest, id=id)

    if claim.item.user == request.user:
        claim.status = 'Rejected'
        claim.save()
        
        # Notify claimer
        Notification.objects.create(
            user=claim.user,
            message=f"❌ Your claim for '{claim.item.title}' was rejected.",
            is_read=False
        )
        messages.success(request, 'Claim rejected successfully.')
    else:
        messages.error(request, 'You are not allowed to reject this claim.')

    return redirect('/dashboard/')


# ✅ DASHBOARD WITH ANALYTICS & CLAIM HISTORY
@login_required(login_url='login')
def dashboard(request):
    # User's items
    my_items = Item.objects.filter(user=request.user).order_by('-id')
    
    # All claims on user's items
    claims = ClaimRequest.objects.filter(item__user=request.user).order_by('-id')
    
    # Claims made by user
    my_claims = ClaimRequest.objects.filter(user=request.user).order_by('-id')
    
    # Analytics
    total_items = my_items.count()
    resolved_items = my_items.filter(is_resolved=True).count()
    total_claims = claims.count()
    pending_claims = claims.filter(status='Pending').count()
    
    context = {
        'my_items': my_items,
        'claims': claims,
        'my_claims': my_claims,
        'total_items': total_items,
        'resolved_items': resolved_items,
        'total_claims': total_claims,
        'pending_claims': pending_claims,
    }
    
    return render(request, 'dashboard.html', context)


# ✅ NOTIFICATIONS
@login_required(login_url='login')
def notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notes.filter(is_read=False).count()
    
    # Mark all as read when viewing
    notes.filter(is_read=False).update(is_read=True)
    
    context = {
        'notes': notes,
        'unread_count': unread_count,
    }
    
    return render(request, 'notifications.html', context)


# ✅ GET UNREAD NOTIFICATION COUNT (for navbar)
def get_unread_count(request):
    if request.user.is_authenticated:
        return Notification.objects.filter(user=request.user, is_read=False).count()
    return 0