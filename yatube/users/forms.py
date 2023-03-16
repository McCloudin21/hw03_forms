from django.contrib.auth.forms import (UserCreationForm,
                                       PasswordChangeForm,
                                       PasswordResetForm,
                                       )
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ChangeForm(PasswordChangeForm):
    def passwordchange(self, user):
        model = User
        fields = ('current password', 'new_password', 'new_password_repeated')


class ResetForm(PasswordResetForm):
    def password_reset(self, user):
        model = User
        fields = ('new_password', 'new_password_confirm')
