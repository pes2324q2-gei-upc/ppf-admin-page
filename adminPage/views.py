from django.http import HttpResponse
from django.db.models import Subquery, OuterRef, Count
from django.shortcuts import render
from common.models.user import Driver, Report, User 

# Create your views here.

def home(request):
    return render(request,'views/home.html')


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
    


