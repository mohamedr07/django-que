from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})


def queue(request, queue_id):
    return render(request, 'queue.html', {
        'queue_id': queue_id
    })
