from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    """Custom form used to creating users
    in Django's Admin when using a custom
    user model"""

    class Meta:
        model = get_user_model()
        fields = ['username']


class CustomUserChangeForm(UserChangeForm):
    """Custom form used to updating users
    in Django's Admin when using a custom
    user model"""

    class Meta:
        model = get_user_model()
        fields = '__all__'
