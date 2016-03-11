# coding=utf-8
import os
import datetime
import re
from django.shortcuts import render
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'checker/index.html', {'page_name': 'checker.index'})


def stats(request):
    return render(request, 'checker/stats.html', {'page_name': 'checker.stats'})
