from django.shortcuts import render
from django.http import HttpResponse

import json
from apps.assets import core


# Create your views here.


def asset_with_no_asset_id(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        print(request.POST.get('asset_data'))

        return HttpResponse('fdsfdsfdsfd')
