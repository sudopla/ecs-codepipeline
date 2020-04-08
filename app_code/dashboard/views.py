from django.shortcuts import render
from django.views.generic import TemplateView

from django.http import JsonResponse
import json

from dashboard.lib.aws import *

# Create your views here.
class IndexView(TemplateView):

    def get(self, request, **kwargs):
        return render(request, 'index.html')


class AWSView(TemplateView):

    def get(self, request, **kwargs):
        return render(request, 'aws.html')


def get_aws_running_instances_types(request):
    aws = AWS()
    results = aws.get_running_instances_types()
    return JsonResponse(results)


def get_aws_storage(request):
    aws = AWS()
    results = aws.get_aws_storage()
    return JsonResponse(results)


def get_aws_storage_monthly(request):
    aws = AWS()
    results = aws.get_aws_storage_monthly()
    return JsonResponse(results)


def get_aws_monthly_costs(request):
    aws = AWS()
    results = aws.get_aws_monthly_costs()
    return JsonResponse(results)

