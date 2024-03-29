from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action, api_view,permission_classes
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework import status

from store.models import Product, Banner, SiteConfig, Testimonial, Transaction, Brands, AboutUs, ContactUs
from store.serializers import ( UserSerializer, BannerSerializer, ProductSerializer,
                               BrandSerializer,SiteConfigSerializer,TestimonialSerializer,CartSerializer,
                               CheckoutSerializer,AboutUsSerializer, ContactUsSerializer)


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.create_user(username=username, email=email, password=password)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'})

def csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})




class ProductPurchaseException(APIException):
    status_code = 405
    default_detail = {
        "code": status_code,
        "message": "Unable to complete purchase - no inventory",
    }


def log_error(error_name, error_message, product):
    print(
        json.dumps(
            {
                "severity": "ERROR",
                "error": error_name,
                "message": f"{error_name}: {error_message}",
                "method": "ProductViewSet.purchase()",
                "product": product.id,
                "countRequested": 1,
                "countFulfilled": product.inventory_count,
            }
        )
    )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    class ProductPurchaseException(APIException):
        status_code = 405
        default_detail = {
            "code": status_code,
            "message": "Unable to complete purchase - no inventory",
        }

    @action(detail=True, methods=["get", "post"])
    def purchase(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        if product.inventory_count > 0:
            product.inventory_count -= 1
            product.save()
            Transaction.objects.create(
                datetime=timezone.now(), product_id=product, unit_price=product.price
            )
        else:
            log_error(
                "INVENTORY_COUNT_ERROR",
                "A purchase was attempted where there was insufficient inventory to fulfil the order.",
                product,
            )
            raise ProductPurchaseException()

        # If the transaction caused a product to sell out, log an error
        if product.inventory_count == 0:
            log_error(
                "INVENTORY_SOLDOUT_ERROR",
                "A purchase just caused a product to sell out. More inventory will be required.",
                product,
            )

        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    
class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class bannerView(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    #handle exceptions
    class BrandsException(APIException):
        status_code = 405
        default_detail = {
            "code": status_code,
            "message": "Unable to load the available brands. Or they are no brands available",
        }
    @action(detail=True, methods=["get", "post"])
    def banner(self, request, pk):
        banner = get_object_or_404(Banner, id=pk)

        if banner.available_count > 1:
            # Return all available banner 
            brands = Brand.objects.all()
            serializer = self.get_serializer(banner, many=True)
            return Response(serializer.data)
        elif banner.available_count == 1:
            # Return only the selected banner
            serializer = self.get_serializer(banner)
            return Response(serializer.data)
        else:
            # No available listed banner,  return the above brands with exception
            raise self.BrandsException

    
    
class BrandsView(viewsets.ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializer
    #handle exceptions
    class BrandsException(APIException):
        status_code = 405
        default_detail = {
            "code": status_code,
            "message": "Unable to load the available brands. Or they are no brands available",
        }
    @action(detail=True, methods=["get", "post"])
    def brands(self, request, pk):
        brand = get_object_or_404(Brand, id=pk)

        if brand.available_count > 1:
            # Return all available brands
            brands = Brand.objects.all()
            serializer = self.get_serializer(brands, many=True)
            return Response(serializer.data)
        elif brand.available_count == 1:
            # Return only the selected brand
            serializer = self.get_serializer(brand)
            return Response(serializer.data)
        else:
            # No available listed brands, return the above brands with exception
            raise self.BrandsException

@api_view(['POST'])
def contact_us_view(request):
    serializer = ContactUsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActiveProductViewSet(viewsets.ViewSet):
    @extend_schema(request=None, responses=ProductSerializer)
    def list(self, request, formatting=None):
        active_product = get_object_or_404(Product, active=True)
        serializer = ProductSerializer(active_product, context={"request": request})
        return Response(serializer.data)


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.order_by("-rating").all()
    serializer_class = TestimonialSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product_id"]


class SiteConfigViewSet(viewsets.ModelViewSet):
    queryset = SiteConfig.objects.all()
    serializer_class = SiteConfigSerializer


class ActiveSiteConfigViewSet(viewsets.ViewSet):
    @extend_schema(responses=SiteConfigSerializer)
    def list(self, request, formatting=None):
        active = get_object_or_404(SiteConfig, active=True)
        serializer = SiteConfigSerializer(active)
        return Response(serializer.data)


@ensure_csrf_cookie
@require_http_methods(["POST"])
def checkout(request):
    def lift_item_status(data):
        status = ""
        for item in data["items"]:
            if "status" in item:
                for i in item["status"]:
                    status = str(i)

        return status

    serializer = CartSerializer(data=json.loads(request.body))

    if not serializer.is_valid():
        status_code = 400
        status = "validation_error"
        if "payment" in serializer.errors:
            status_code = 501
            status = serializer.errors["payment"]["method"][0].code
        if "items" in serializer.errors:
            status = lift_item_status(serializer.errors)
        return JsonResponse(
            {"status": status, "errors": serializer.errors}, status=status_code
        )

    cart = serializer.validated_data

    items = []
    for item in cart["items"]:
        product = get_object_or_404(Product, id=item["id"])
        count = item["countRequested"]

        product.inventory_count -= count
        product.save()
        for _ in range(count):
            Transaction.objects.create(
                datetime=timezone.now(), product_id=product, unit_price=product.price
            )
        items.append(
            {"id": product.id, "countRequested": count, "countFulfilled": count}
        )

        if product.inventory_count == 0:
            log_error(
                "INVENTORY_SOLDOUT_ERROR",
                "A purchase just caused a product to sell out. More inventory will be required.",
                product,
            )

    response = CheckoutSerializer(data={"status": "complete", "items": items})
    response.is_valid()
    return JsonResponse(response.data)


