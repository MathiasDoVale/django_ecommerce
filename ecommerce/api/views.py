from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer,
    ProductSerializer,
    ImageSerializer,
    InventorySerializer,
    CartSerializer,
    OrderSerializer
)
from rest_framework import status
from products.models import Product, Image, Inventory, Cart, Order, OrderItem
################## User ##################

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = None
    if not user:
        user = authenticate(email=email, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    try:
        # Delete the user's token to logout
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
################## Products ##################

@api_view(['GET'])
def home_products(request):
    gender = request.query_params.get('gender', None)
    products = Product.objects.filter(has_item=True).order_by('brand', 'model').distinct('brand', 'model')
    gender_filters = {'man': {'man': True}, 'woman': {'woman': True}, 'girl': {'girl': True}, 'boy': {'boy': True}}
    data = []
    for product in products:
        filter_args = gender_filters.get(gender, {})
        filter_args['product_id'] = product.id
        image = Image.objects.filter(**filter_args).first()
        if image:
            product_serializer = ProductSerializer(product)
            image_serializer = ImageSerializer(image)
            data.append({'product': product_serializer.data, 'image': image_serializer.data})
    try:
        return Response({'data': data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def product_detail(request, product_id_model):
    selected_product = Product.objects.get(id=product_id_model)
    similar_products = Product.objects.filter(brand=selected_product.brand, model=selected_product.model)

    data = []
    for product in similar_products:
        images = Image.objects.filter(product_id=product.id)
        items_inventory = Inventory.objects.filter(product_id=product.id).distinct('size')
        images_serializer = []
        items_inventory_serializer = []
        if images and items_inventory:
            product_serializer = ProductSerializer(product)
            for item in items_inventory:
                item_inventory_serializer = InventorySerializer(item)
                items_inventory_serializer.append(item_inventory_serializer.data)
            for image in images:
                image_serializer = ImageSerializer(image)
                images_serializer.append(image_serializer.data)
            data.append({'product': product_serializer.data, 'images': images_serializer, 'items_inventory': items_inventory_serializer})
    return Response({'data': data}, status=status.HTTP_200_OK)


################## Cart ##################
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(request):
    if request.method == 'GET':
        cart_items = Cart.objects.filter(user=request.user, active=True)
        data = []

        total_price = 0
        for item in cart_items:
            product = Product.objects.get(id=item.product_id)
            total_price = product.price + total_price
            image = Image.objects.filter(product_id=product.id).first()

            product_serializer = ProductSerializer(product)
            image_serializer = ImageSerializer(image)
            item_cart_serializer = CartSerializer(item)
            data.append({'cart_item_id': item_cart_serializer.data, 'product': product_serializer.data, 'image': image_serializer.data})

        return Response({'data': data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        size = request.POST.get('size')
        # Check if item is in stock
        inventory = Inventory.objects.filter(product_id=product_id, size=size)
        if inventory.exists():
            # Add item to cart
            Cart.objects.create(user=request.user, product=product, size=size)
        return Response({'message': 'Item added to cart'}, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        cart_item_id = request.data.get('cart_item_id')
        Cart.objects.get(id=cart_item_id).delete()
        return Response({'message': 'Item deleted from cart'}, status=status.HTTP_200_OK)
    

################## Checkout ##################
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    if request.method == 'GET':
        cart_items = Cart.objects.filter(user=request.user, active=True)
        data = []

        total_price = 0
        for item in cart_items:
            product = Product.objects.get(id=item.product_id)
            total_price = product.price + total_price
            image = Image.objects.filter(product_id=product.id).first()

            product_serializer = ProductSerializer(product)
            image_serializer = ImageSerializer(image)
            item_cart_serializer = CartSerializer(item)
            data.append({'cart_item_id': item_cart_serializer.data, 'product': product_serializer.data, 'image': image_serializer.data})

        return Response({'data': data}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        cart = Cart.objects.filter(user=request.user, active=True)
        order = Order.objects.create(user=request.user)
        # Payment logic goes here
        for item in cart:
            try:
                item_inventory = Inventory.objects.filter(product_id=item.product, size=item.size).first()
            except Inventory.DoesNotExist:
                return Response({'message': "Item is not in stock: "+ str(item.product.brand) + str(item.product.model) + str(item.size)}, status=status.HTTP_400_BAD_REQUEST)
            
            OrderItem.objects.create(
                item_inventory=item_inventory,
                order=order,
                quantity=1
            )
            item.active = False
            item.save()
        items = OrderItem.objects.filter(order=order)

        for item in items:
            if hasattr(item, 'item_inventory') and item.item_inventory:
                Inventory.delete_item(item.item_inventory.product_id, item.item_inventory.id)
        order.state = 'PAYED'
        order.save()
        order_serializer = OrderSerializer(order)
        return Response({'data': order_serializer.data}, status=status.HTTP_200_OK)