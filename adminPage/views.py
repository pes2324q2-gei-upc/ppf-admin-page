from django.forms import model_to_dict
from django.db.models import Subquery, OuterRef, Count
from django.shortcuts import get_object_or_404, render
from common.models.user import Driver, Report, User

# Create your views here.


def home(request):
    return render(request, 'views/home.html')


def users(request):
    users = User.objects.all()
    search_filter = request.GET.get('searching')

    if search_filter:
        users = users.filter(username__icontains=search_filter)

    return render(request, "views/users.html", {"users": users})


def reported(request):
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


def userReportsDetails(request, pk):
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
    return render(request, 'views/report_details.html', {'report': report})
