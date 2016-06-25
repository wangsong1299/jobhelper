#! -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json
from datetime import datetime
import logging



def toInteger(data):
    try:
        return int(data)
    except:
        return None

def toFloat(data):
    try:
        return float(data)
    except:
        return None

def toDateTime(data):
    try:
        return datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
    except:
        return None

def toDate(data):
    try:
        return datetime.strptime(data, '%Y-%m-%d')
    except:
        return None

def round2(data):
    try:
        return round(data, 2)
    except:
        return None

################################################################################



def message(msg, code):
    return json.dumps(dict(message = msg, code = code))


def baseresponse(msg, code):
    return HttpResponse(message(msg, code), content_type = 'application/json')


def encode_utf8(value): 
    if isinstance(value, unicode):
        return value.encode('utf8')
    return value

def decode_utf8(value):
    if isinstance(value, str):
        return value.decode('utf8')
    return value


###############################################################################


def split_page(objects, page, num_per_page):
    try:
        paginator = Paginator(objects, num_per_page)
        result = paginator.page(page)
    except PageNotAnInteger, e:
        logging.warn(e)
        result = paginator.page(1)
    except EmptyPage, e:
        logging.warn(e)
        return []

    return result.object_list
        
################################################################################ 



