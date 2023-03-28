from django.shortcuts import render
from .models import documents

def index_documents(request):
    all = documents.all_elements(now_house = request.session['house_id'])

    return render(
            request,
            'index_documents.html',
            context = {"all" : all},
    )

def only_codex(request):
    type_y = documents.choose_elements(now_type = "Устав", now_house = request.session['house_id'])
    return render(
            request,
            'codex.html',
            context = {"type_y" : type_y},
    )

def only_protocols(request):
    type_p = documents.choose_elements(now_type = "Протокол", now_house = request.session['house_id'])
    return render(
            request,
            'protocols.html',
            context = {"type_p" : type_p},
    )