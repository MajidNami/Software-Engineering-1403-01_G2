import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))) 
from group1.management.handle import handle_login, handle_register



from django.shortcuts import render, redirect
from django.contrib import messages




def group_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            error_message = 'Both username and password are required.'
            return render(request, 'login.html', {'error': error_message})

        response = handle_login(username, password)

        print(response)  # Debug purpose

        if response == "Login successful.":
            next_url = request.GET.get('next', 'group1:autocomplete_page')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': response})

    return render(request, 'login.html')


def group_register_view(request):
    if request.method == 'POST':
        
        username = request.POST.get('username', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        age = request.POST.get('age', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        print("test")
        if not username or not name or not email or not age or not password1 or not password2:
            error_message = 'All fields are required. Please fill in all fields.'
            return render(request, 'signup.html', {'error': error_message, 'username': username, 'name': name, 'email': email, 'age': age})

        
        response = handle_register(username, name, email, age, password1, password2)

        #print(response)


        if response == "Registration successful. Please login.":
            # Redirect to the login page on success
            return redirect("group1:group_login")
        else:
            # Render the signup page with the error message
            return render(request, 'signup.html', {'error': response, 'username': username, 'name': name, 'email': email, 'age': age})

    return render(request, 'signup.html')
