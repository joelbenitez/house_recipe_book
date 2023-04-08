from django.contrib import messages
from django.contrib.auth.decorators import login_required

# from django.core.mail import EmailMessage, send_mail
from django.shortcuts import redirect, render

from .forms import UpdateProfileForm  # CustomerInterconnectionForm,
from .forms import UserRegistrationForm, UserUpdateForm

# Create your views here.


# def register(request):
#     if request.method == "POST":
#         form = CustomerInterconnectionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             messages.success(request, f"Account created for {username}")
#             return redirect("blog-home")
#     else:
#         form = CustomerInterconnectionForm()
#     return render(request, "users/register.html", {"form": form, "title": "Register"})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            # new_user_email = form.cleaned_data.get("email")

            # Sending email to notify user an account has been created
            # send_mail(
            #     subject="Your account has been successfully created",
            #     message=f"Your username: {username}\n\nThank you for joining!",
            #     from_email="Do-Not-Reply<donotreply@chuspi.com>",
            #     recipient_list=[new_user_email],
            #     fail_silently=True,
            # )

            # # Sending email with attachments
            # attachments = []
            # filename = "menu_example.pdf"
            # content = open(filename, "rb").read()
            # attachment = (filename, content, "application/pdf")
            # attachments.append(attachment)

            # email_body = "This is a test of the menu delivery system. Please let us know which days work for you."

            # email = EmailMessage(
            #     subject="Menu for the week",
            #     body=email_body,
            #     from_email="Do-Not-Reply<donotreply@chuspi.com>",
            #     to=[
            #         "joelbenitez90@gmail.com",
            #         # "mniewinski1130@gmail.com",
            #         # "nicoleniewinski@aol.com",
            #     ],
            #     attachments=attachments,
            # )
            # email.send()

            messages.success(
                request, f"Your account has been created, {username}. Please log in!"
            )
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "users/newuser.html", {"form": form, "title": "Register"})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, "Your account has been updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }

    return render(request, "users/profile.html", context)
