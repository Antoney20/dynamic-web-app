from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

from store import views


router = DefaultRouter()

router.get_api_root_view().cls.__name__ = "Antony Server"
router.get_api_root_view().cls.__doc__ = (
    "This is the Django REST Framework API, serving all endpoints."
)

router.register(r"products", views.ProductViewSet, basename="product")
#brands
router.register(r"Brands", views.BrandsView, basename="brand")
router.register( r"active/product", views.ActiveProductViewSet, basename="active_product")
router.register(r"testimonials", views.TestimonialViewSet, basename="testimonial")
router.register(r"site_config", views.SiteConfigViewSet, basename="site_config")
router.register( r"active/site_config", views.ActiveSiteConfigViewSet, basename="active_siteconfig")

urlpatterns = [
    path("", include(router.urls)),
    path("checkout", views.checkout, name="checkout"),
    path("csrf_token", views.csrf_token, name="csrf_token"),
    path('contact-us/', views.contact_us_view, name='contact_us_view'),
    path("api-auth/", include("rest_framework.urls")),
]