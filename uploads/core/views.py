from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.models import Document
from uploads.core.forms import DocumentForm
from uploads.core.functions import handle_uploaded_file


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })


def simple_upload(request):
    allowedIps = ['129.0.0.1', '127.0.0.1']
    user_ip = request.META['REMOTE_ADDR']
    print("user_ip:", user_ip) 
    
    for ip in allowedIps:
            print("ip:",ip)
            if ip==user_ip:
                if request.method == 'POST' and request.FILES['myfile']:
                    myfile = request.FILES['myfile']
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name, myfile)
                    print("filename:", filename)        
                    uploaded_file_url = fs.url(filename)       
                    print("uploaded_file_url:", uploaded_file_url)
                    
                    
                    
                    handle_uploaded_file(uploaded_file_url.lstrip('/'))
                    
                    outName = uploaded_file_url.split(".",1)
                    fout = outName[0] + ".csv"
                    
                    return render(request, 'core/simple_upload.html', {
                        'uploaded_file_url': fout
                    })
                #else:
                return render(request, 'core/simple_upload.html')         
    
    print("invalid ip address")
    return render(request, 'core/error.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
