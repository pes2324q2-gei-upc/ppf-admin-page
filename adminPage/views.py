from django.forms import model_to_dict
from django.db.models import Subquery, OuterRef, Count
from django.shortcuts import get_object_or_404, redirect, render
import requests
from common.models.user import Driver, Report, User
from rest_framework.authtoken.models import Token
from adminPage.forms import UserForm
from django.contrib.auth.hashers import make_password

# create generic functions


def sendDeleteRequest(user, token=None, url=None):
    """
    Sends a DELETE request to the specified URL with the provided token as authorization.

    Parameters:
    user (User): The User object for which the token is retrieved.
    token (Token, optional): The Token object to use for authorization. Defaults to the token associated with the provided user.
    url (str): The URL to send the DELETE request to.

    Raises:
    ValueError: If the URL or token key is not a string.

    Returns:
    requests.Response: The response object from the DELETE request.
    """
    if not token:
        token = Token.objects.get(user=user)

    # Ensure that url is a string
    if not isinstance(url, str):
        raise ValueError(f"url must be a string\nURL: {url}")

    # Ensure that token.key is a string
    if not isinstance(token.key, str):
        raise ValueError("token.key must be a string")

    # Concatenate 'Token ' and token.key
    auth_header = 'Token ' + token.key

    return requests.delete(url=url, headers={'Authorization': auth_header})


def deleteUser(user):
    """
    Deletes the specified user.
    """
    url = 'http://user-api:8000/users/' + \
        str(user.pk)

    return sendDeleteRequest(user, url=url)


def home(request):
    return render(request, 'views/home.html')


def users(request):
    users = User.objects.all()
    search_filter = request.GET.get('searching')

    if search_filter:
        users = users.filter(username__icontains=search_filter)

    return render(request, "views/users.html", {"users": users})


def reported(request):
    """
    Displays a list of users who have been reported.
    """
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        userId = request.POST.get('userId')
        user = get_object_or_404(User, pk=userId)
        deleteUser(user)
        return redirect('reports')

    # Subquery to count the number of reports for each user
    report_counts = Report.objects.filter(reported_id=OuterRef('id')).values('reported_id').annotate(
        report_count=Count('id')
    ).values('report_count')

    # Annotate each user queryset with the report count using the subquery
    users = User.objects.annotate(report_count=Subquery(report_counts))

    # Filter users who have been reported at least once
    users = users.filter(report_count__gt=0).order_by('-report_count')

    search_filter = request.GET.get('searching')

    if search_filter:
        users = users.filter(username__icontains=search_filter)

    return render(request, "views/reported.html", {"users": users})


def userDetails(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_dict = model_to_dict(user)  # type: ignore

    search_filter = request.GET.get('searching')
    if search_filter:
        searched_dict = {}
        for key, value in user_dict.items():
            if search_filter.lower() in key.lower() or search_filter.lower() in str(value).lower():
                searched_dict[key] = value
            elif user and hasattr(user, key) and str(getattr(user, key)).lower().find(search_filter.lower()) != -1:
                searched_dict[key] = value
        user_dict = searched_dict

    return render(request, 'views/user_details.html', {'user': user, 'user_data': user_dict})


def userDetailsEdit(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            # Check if the password field is present and not hashed
            if 'password' in form.cleaned_data and not form.cleaned_data['password'].startswith('$'):
                form.cleaned_data['password'] = make_password(
                    form.cleaned_data['password'])
            form.save()
            return redirect('userDetails', pk=pk)
    else:
        form = UserForm(instance=user)

    return render(request, 'views/user_details_edit.html', {'form': form, 'user': user})


def userReportsDetails(request, pk):
    """
    Displays a list of reports for the specified user.
    """
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        user = get_object_or_404(User, pk=pk)
        deleteUser(user)
        return redirect('userReportsDetails', pk)

    user = get_object_or_404(User, pk=pk)
    reports = Report.objects.filter(reported_id=pk)
    reports_count = reports.count()

    search_filter = request.GET.get('searching')
    if search_filter:
        user_set = User.objects.filter(username__icontains=search_filter)
        reports = reports.filter(reporter__in=user_set)
    return render(request, 'views/user_report_details.html', {'user': user, 'reports': reports, 'reports_count': reports_count})


def reportDetails(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        reportedId = str(report.reported.pk)
        report.delete()
        return redirect('userReportsDetails', reportedId)
    return render(request, 'views/report_details.html', {'report': report})
