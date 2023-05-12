from django.shortcuts import render


def handler404(request, exception):
    """ 
    This function shows a customized 404 error page
     """
    return render(request, '404.html', status=404)


def server_error(request):
    """
        This function shows a customized 500 error page
    """
    return render(request, 'errors/500.html', status=500)
