from django.urls import path
from .views import CheckPluginUpdateAPIView  # Import the view class

urlpatterns = [
    path('wp/plugins/check-updates', CheckPluginUpdateAPIView.as_view(), name='check_updates'),  # Add a URL pattern for the view
]


# http://<your-domain>/wp/plugins/check-updates/?license_key=your_license_key&plugin_name=your_plugin_name
