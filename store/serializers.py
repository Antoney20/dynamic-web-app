import json

from rest_framework import serializers
from store.models import Banner,Product, SiteConfig, Testimonial, Brands, AboutUs, ContactUs
from django.contrib.auth.models import User

from .models import Profile

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "discount_price",
            "active",
            "discount_percent",
            "discount_saving",
            "inventory_count",
            "image",
        ]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            "id",
            "product_id",
            "reviewer_name",
            "reviewer_location",
            "rating",
            "summary",
            "description",
        ]


class SiteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfig
        fields = [
            "active",
            "color_primary",
            "color_secondary",
            "color_action",
            "color_action_text",
            "site_name",
            "site_name_font",
            "site_name_color",
            "base_font",
        ]
        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = [
            "id",
            "name",
            "Description",
            "image",
        ]
        
class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = [
            "id",
            "tittle",
            "content",
            "image",
            "created_at",
            "updated_at",
        ]

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = [
            "id",
            "name",
            "email",
            "subject",
            "message",
            "created_at",
        ]

class CartPaymentSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=["collect"])


class CartCustomerSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    countRequested = serializers.IntegerField(required=True)
    countFulfilled = serializers.IntegerField(required=False)

    def validate(self, data):
        try:
            product = Product.objects.get(pk=data["id"])
        except Product.DoesNotExist:
            raise serializers.ValidationError(detail={"status": "product_not_found"})

        requested = data["countRequested"]
        if product.inventory_count < requested:
            data["countFulfilled"] = product.inventory_count

            # Log error by writing structured JSON. Can be then used with log-based alerting, metrics, etc.
            error_name = "INSUFFICIENT_PRODUCT_ERROR"
            print(
                json.dumps(
                    {
                        "severity": "ERROR",
                        "error": error_name,
                        "message": f"{error_name}: A purchase was attempted where there was insufficient inventory to fulfil the order.",
                        "product": product.id,
                        "method": "CartItemSerializer.validate()",
                        "countRequested": data["countRequested"],
                        "countFulfilled": data["countFulfilled"],
                    }
                )
            )

            raise serializers.ValidationError(
                detail={"status": "insufficient_product", "items": data}
            )
        else:
            data["countFulfilled"] = requested
        return data


class CartSerializer(serializers.Serializer):
    customer = CartCustomerSerializer(required=True)
    payment = CartPaymentSerializer(required=True)
    items = CartItemSerializer(many=True)


class CheckoutSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    status = serializers.CharField()