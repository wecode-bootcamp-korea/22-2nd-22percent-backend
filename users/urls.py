from django.urls    import path

from users.views    import EmailSignupView

urlpatterns = [
    path('/signup/email', EmailSignupView.as_view()),
]
