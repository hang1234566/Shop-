from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from .models import Category, Product, Review
from .forms import ReviewForm, ProductSearchForm

def home(request):
    """Home page view showing featured products."""
    featured_products = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def product_list(request, category_slug=None):
    """View to display products, optionally filtered by category."""
    category = None
    products = Product.objects.filter(available=True)
    form = ProductSearchForm(request.GET)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Handle search and filtering
    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)
    
    context = {
        'category': category,
        'products': products,
        'form': form,
    }
    
    return render(request, 'products/product_list.html', context)

def product_detail(request, id, slug):
    """View to display product details and handle reviews."""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Handle review submission
    review_form = None
    user_review = None
    
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if request.method == 'POST':
            # User is submitting or updating a review
            if user_review:
                review_form = ReviewForm(request.POST, instance=user_review)
            else:
                review_form = ReviewForm(request.POST)
                
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                return redirect('products:product_detail', id=id, slug=slug)
        else:
            # Display the form with existing review if any
            review_form = ReviewForm(instance=user_review) if user_review else ReviewForm()
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_form': review_form,
        'user_review': user_review,
    }
    
    return render(request, 'products/product_detail.html', context)

def category_list(request):
    """View to display all categories."""
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})
