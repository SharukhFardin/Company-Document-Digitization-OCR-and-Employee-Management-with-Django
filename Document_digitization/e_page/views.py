from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from admin_page.models import *
from django.contrib.sessions import *
from admin_page.views import login_d
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404

#Method for Employee Page
def e_page(request):
    # session_email = request.session['user']
    try:
        session_email = login_d['user']
    except:
        messages.info(request, "Please login again")
        return render(request, 'login.html')
    user = Plan_User.objects.get(email = session_email)
    name = user.name
    args = {} #pyhton dictionary
    args['xy']=name #adding key and value in dictionary

    #database table row counting
    tu = Plan_User.objects.count()
    tg = User_Group.objects.count()
    args["tu"]=tu
    args["tg"]=tg

    return render(request, 'e_page.html', args)

#Method for file management in employee page
def e_files(request):
    try:
        session_email = login_d['user']
    except:
        messages.info(request, "Please login again")
        # return redirect('login')
        return render(request, 'login.html')
    user = Plan_User.objects.get(email = session_email)
    ugroup = User_Group.objects.get(id=user.group_id.id)
    file = Doc_Files.objects.filter(group_id=user.group_id).all()

    dic = {'id':ugroup.id, 'name':ugroup.group_name, 'file':file}

    if request.method =='POST':
        #Exception handling for getting logged in user info
        try:
            session_email = login_d['user']
        except:
            messages.info(request, "Please login again")
            return render(request, 'login.html')

        #Getting user and file info's
        uploaded_file = request.FILES['document'] #Getiing the uploaded file and storing in a variable
        name = uploaded_file.name
        user = Plan_User.objects.get(email = session_email)
        gid = user.group_id.id
        group = User_Group.objects.get(id = gid)

        #Storing the info's in database
        indatabase = Doc_Files(name=name, doc=uploaded_file, user_id=user, group_id=group)
        indatabase.save() #saving instance to database

        #Send Notification to the Manager
        uname = user.name
        msg1 = uname + ", has uploaded a file named : " + name

        n1 = Notification(message = msg1, user_g_id = group.id)
        n1.save()

        n1.user.add(user)
        n1.save()
        ##

        # obj = FileSystemStorage()
        # obj.save(uploaded_file.name, uploaded_file)
    return render(request, 'e_files.html', dic)

#Method for viewing pdf
def pdf_view(request):

    if 'btn1' in request.GET:
        pdfname = request.GET['pdfname']
        str = 'media/Files/'+pdfname
        try:
            return FileResponse(open(str, 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()
    elif 'btn2' in request.GET:
        pdfname = request.GET['pdfname']
        pdfobj = Doc_Files.objects.get(name=pdfname)
        if pdfobj.doc:
            pdfobj.doc.delete()
        pdfobj.delete()
        messages.info(request, "Your file deleted")

        #Send Notification to the Manager
        uname = user.name
        msg1 = uname + ", has Deleted a file named : " + pdfname

        n1 = Notification(message = msg1, user_g_id = group.id)
        n1.save()

        n1.user.add(user)
        n1.save()
        ##

    return redirect('e_files')

#Method for employee notification
def E_notification(request):
    return render(request, "E_notification.html")
