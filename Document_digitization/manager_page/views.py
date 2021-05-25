from django.shortcuts import render, redirect
from django.contrib import messages
from admin_page.models import *
from django.contrib.sessions import *
from admin_page.views import login_d

# Method for the manager page redirection and more
def manager_page(request):
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


    mid = user.id
    gs = User_Group.objects.filter(creator = mid)
    l=[]
    c=0
    for i in gs:
        l.append(gs[c].id)
        c+=1

    flist = []
    for i in l:
        file = Doc_Files.objects.filter(group_id=i).all()
        flist.append(file)

    args['fl']=flist

    return render(request, "manager_page.html" , args)

#Method for the manager profile
def manager_profile(request):
    # session_email = request.session['user']
    try:
        session_email = login_d['user']
    except:
        messages.info(request, "Please login again")
        return render(request, 'login.html')
    user = Plan_User.objects.get(email = session_email)
    mid = user.id
    gs = User_Group.objects.filter(creator = mid)
    l=[]
    c=0
    for i in gs:
        l.append(gs[c].group_name)
        c+=1

    ava = user.avatar
    pimg = avatar.objects.get(id=ava)
    allava = avatar.objects.all()

    args = {'name':user.name,'email':user.email,'id':user.id, 'role':user.role_id.role, 'grps':l, 'avatar':pimg, 'allava':allava,} #adding key and value in dictionary

    #notification to admin for changing password
    name = user.name
    msg1 = name + ", has changed his password"

    # if request.method=="POST":
    if "btn1" in request.POST:
        oldp=request.POST["oldpass"]
        newp=request.POST["newpass"]
        repeat=request.POST["repeat"]

        dbpass = user.password
        #This section does the password change for the manager
        if dbpass==oldp:
            if newp==repeat:
                uid=user.id
                Plan_User.objects.filter(id=uid).update(password=newp)
                messages.info(request, "You have changed your password")

                n1 = Notification(message = msg1)
                n1.save()

                n1.user.add(user)
                n1.save()

            else:
                messages.info(request, "Give same password for new and repeat password")
        else:
            messages.info(request, "You have given wrong password")
    #This section does the group deletion
    elif "btn2" in request.POST:
        gname=request.POST["gname"]
        gss = User_Group.objects.filter(group_name=gname)
        g_id = gss[0]
        none_g = User_Group.objects.get(group_name='None')
        e_in_g = Plan_User.objects.filter(group_id=g_id)
        for i in e_in_g:
            idd=i.id
            Plan_User.objects.filter(id=idd).update(group_id=none_g.id)
        gss.delete()
        messages.info(request, "Group deleted")

    #This section does the avatar update for manager
    elif "btn3" in request.POST:
        iid = request.POST['iid']
        avtr = request.FILES['avatar']

        indb = avatar(id=iid,name=avtr)
        indb.save()

        Plan_User.objects.filter(id=user.id).update(avatar=iid)

        # Plan_User.objects.filter(id=user_id).update(avatar=avatar)
        messages.info(request, "Avatar Successfully Updated")
        return redirect("manager_profile")

    elif request.POST:
        proimg = request.POST["pimg"]
        Plan_User.objects.filter(id=user.id).update(avatar=proimg)
        return redirect("manager_profile")

    return render(request, "manager_profile.html", args)

#Method for creating groups for manager
def c_group(request):
    try:
        session_email = login_d['user']
    except:
        messages.info(request, "Please login again")
        # return redirect('login')
        return render(request, 'login.html')
    user = Plan_User.objects.get(email = session_email)
    mid = user.id

    if request.method=="POST":
        Gid = request.POST["gid"]
        Gname = request.POST["gname"]
        u1 = request.POST["ucidw"]
        u2 = request.POST["ucidx"]
        u3 = request.POST["ucidy"]
        u4 = request.POST["ucidz"]

        ingtable = User_Group(id=Gid, group_name=Gname, creator=mid, total_members=4)
        ingtable.save()

        Plan_User.objects.filter(id=u1).update(group_id=ingtable.id)
        Plan_User.objects.filter(id=u2).update(group_id=ingtable.id)
        Plan_User.objects.filter(id=u3).update(group_id=ingtable.id)
        Plan_User.objects.filter(id=u4).update(group_id=ingtable.id)

        #Send Notification to the admin
        name = user.name
        msg1 = name + ", has created a group named " + Gname

        n1 = Notification(message = msg1)
        n1.save()

        n1.user.add(user)
        n1.save()
        ##

        messages.info(request, "Group successfully created")

    results=Plan_User.objects.all

    return render(request, "c_group.html", {'userid':results}, )

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

    return redirect('manager_page')

# Method for manager notification
def M_notification(request):
    try:
        session_email = login_d['user']
    except:
        messages.info(request, "Please login again")
        return render(request, 'login.html')

    user = Plan_User.objects.get(email = session_email)

    g_id = user.group_id.id #get the group id
    print(g_id)

    Notify = reversed(Notification.objects.filter(user_g_id=g_id).all()) #find out the notifications belong to the groups

    args = {'Notification' : Notify}

    return render(request, "M_notification.html", args)
