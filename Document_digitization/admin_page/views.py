from django.shortcuts import render, redirect
from django.contrib import messages
from admin_page.models import *
from django.contrib.sessions import *
from Document_digitization.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import PyPDF2
from difflib import SequenceMatcher

'''
from django.views.generic import TemplateView

class admin_page(TemplateView):
    template_name = 'admin_page.html'

class Create_user(TemplateView):
    template_name = 'Create_user.html'
'''

#Creating a session for storing login info.
login_d={}

#Method for User Login and validation
def login(request):
    #If user is logged in
    if login_d:
        try:
            session_email = login_d['user']
        except:
            messages.info(request, "Please login again")
            return render(request, 'login.html')
        user = Plan_User.objects.get(email = session_email)
        if (user.role_id.id == 1): #soecufying the foreign table value by role_id.id
            return redirect('admin_page')
        elif (user.role_id.id == 2):
            return redirect('manager_page')
        else:
            return redirect('e_page')

    #If user is not logged in check validation
    elif request.method == 'POST' :
        user_email = request.POST['email']
        user_password = request.POST['password']

        #if email is not enlisted the query won't work. Therefor this exception handling is used.
        try:
            user = Plan_User.objects.get(email = user_email)
        except:
            messages.info(request, "Invalid Email or Password")
            return render(request, 'login.html')

        #Check User by if else conditions
        name = user.name
        role_id = user.role_id.id

        #Redirect users to their landing pages
        if (user.isactive == True): #Check if the user is already active.
            login_d['user'] = user_email
            if (user.role_id.id == 1): #soecufying the foreign table value by role_id.id
                return redirect('admin_page')
            elif (user.role_id.id == 2):
                 return redirect('manager_page')
            else:
                return redirect('e_page')

        elif(user.email == user_email) and (user.password == user_password) and (user.isactive == False): #Verify user

            user.isactive = True
            user.save()
            login_d['user'] = user_email #Stores login_email info in a session
            if (user.role_id.id == 1):
                return redirect('admin_page')
            elif (user.role_id.id == 2):
                return redirect('manager_page')
            else:
                return redirect('e_page')

        else: #If wrong login info is provided
            messages.info(request, "Invalid Email or Password")
            return redirect('login')

    else :
        return render(request, "login.html")

#Method for redirecting to the admin page and more
def admin_page(request):
    try:
        session_email = login_d['user']
    except:
        messages.info(request, "Please login again")
        return render(request, 'login.html')
    # session_email = request.session['user']

    user = Plan_User.objects.get(email = session_email)
    name = user.name
    args = {} #pyhton dictionary
    args['xy']=name #adding key and value in dictionary

    #database table row counting
    tu = Plan_User.objects.count()
    tg = User_Group.objects.count()
    args["tu"]=tu
    args["tg"]=tg

    return render(request, "admin_page.html", args)

#Creating a new user method in admin page
def Create_user(request):

    if request.method=="POST":
        name = request.POST["Name"]
        Id = request.POST["Id"]
        email = request.POST["Email"]
        password = request.POST["psw"]
        role_name = request.POST["Role"] #role_name

        r_id = User_Role.objects.filter(role=role_name) #Role table filtering using given role_id

        gob = User_Group.objects.get(id=1) #creating Group model class object for getting a default value from Group table

        #Now to write in database creating a instance for User class from model
        indatabase = Plan_User(id=Id, name=name, email=email, password=password, userlink="TBA", group_id=gob, role_id=r_id[0])
        indatabase.save() #saving instance to database

        #sending mail to user
        subject = 'Congratulation from Plan International'
        message = 'Hi, '+name+',\n'+'Welcome to our family. You are a new member of ours now!!'+'\n'+'Your user id: '+Id+'\n'+'Your password: '+password+'\n\n'+'Thank you'
        send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently = False)

        messages.info(request, "User account successfully created")

    result = User_Role.objects.all

    return render(request, "Create_user.html", {'roles':result}, )

#User Log Out method
def logout_user(request):
    # session_email = request.session['user'] #Get the stored login info
    try:
        session_email = login_d['user']
    except:
        messages.info(request, "Please login again")
        return render(request, 'login.html')
    user = Plan_User.objects.get(email = session_email) #Figure out the user by that info
    user.isactive = False
    uid=user.id
    Plan_User.objects.filter(id=uid).update(isactive=False)
    user.save()
    del login_d['user']
    messages.info(request, "Successfully Logged Out")
    return render(request, "login.html") #Redirect to the login page
    flush() #Flushes login data

#Method for admin profile
def admin_profile(request):
    # session_email = request.session['user']
    try:
        session_email = login_d['user']
    except:
        messages.info(request, "Please login again")
        return render(request, 'login.html')
    user = Plan_User.objects.get(email = session_email)

    user_ids = Plan_User.objects.all
    # avatar = user.avatar
    # print(avatar)
    ava = user.avatar
    pimg = avatar.objects.get(id=ava)
    allava = avatar.objects.all()

    args = {'name':user.name,'email':user.email,'id':user.id, 'role':user.role_id.role, 'ids':user_ids, 'avatar':pimg, 'allava':allava,} #adding key and value in dictionary

    #This btn1 is the name of Change password button in admin page. The following does the password change for the admin
    if "btn1" in request.POST:
        oldp=request.POST["oldpass"]
        newp=request.POST["newpass"]
        repeat=request.POST["repeat"]

        dbpass = user.password
        if dbpass==oldp:
            if newp==repeat:
                uid=user.id
                Plan_User.objects.filter(id=uid).update(password=newp)
                messages.info(request, "You have changed your password")
            else:
                messages.info(request, "Give same password for new and repeat password")
        else:
            messages.info(request, "You have given wrong password")

    #This section is for deleting an user
    elif "btn2" in request.POST:
        muser=request.POST["muser"]
        deluser = Plan_User.objects.filter(id=muser)

        deluser.delete()
        messages.info(request, "User deleted")

    #This section is for the avatar
    elif "btn3" in request.POST:
        iid = request.POST['iid']
        avtr = request.FILES['avatar']

        indb = avatar(id=iid,name=avtr)
        indb.save()

        # Plan_User.objects.filter(id=user_id).update(avatar=avatar)
        messages.info(request, "Avatar Successfully Updated")
        return redirect("admin_profile")

    elif request.POST:
        proimg = request.POST["pimg"]
        Plan_User.objects.filter(id=user.id).update(avatar=proimg)
        return redirect("admin_profile")


    return render(request, "admin_profile.html", args)

#File Searching
def search_page(request):
    if request.method=="POST":
        search = request.POST["search"]
        search=search.lower()
        allname = Plan_User.objects.values_list('name')
        allid = Plan_User.objects.values_list('id')
        allemail = Plan_User.objects.values_list('email')
        allfile = Doc_Files.objects.values_list('name')
        lname=[]
        lid=[]
        lemail=[]
        lfile = []

        for i in allname:
            lname.append(i[0].lower())
        for i in allid:
            lid.append(i[0])
        for i in allemail:
            lemail.append(i[0])
        for i in allfile:
            lfile.append(i[0])

        d = {'s':search}
        intiger = 0
        try:
            intiger = int(search)
        except:
            intiger = 0
        ps=''
        if search[-3]!='pdf':
            ps = search+'.pdf'

        if search in lname:
            uname = Plan_User.objects.get(name=search)
            d['x'] = [uname.name, uname.id, uname.email, uname.group_id.group_name, uname.role_id.role]

        elif search in lemail:
            uemail = Plan_User.objects.get(email=search)
            d['x'] = [uemail.name, uemail.id, uemail.email, uemail.group_id.group_name, uemail.role_id.role]

        elif intiger in lid:
            usid = Plan_User.objects.get(id=search)
            d['x'] = [usid.name, usid.id, usid.email, usid.group_id.group_name, usid.role_id.role]

        elif ps in lfile:
            fl = Doc_Files.objects.get(name=ps)
            d['fn'] = fl.name
            d['x'] = [fl.name, fl.group_id.group_name, fl.user_id.name]

        else:
            doc = Doc_Files.objects.all()
            pdf = {}
            for file in doc:
                s=''
                str = file.doc
                pread=PyPDF2.PdfFileReader(str)
                for page in range(pread.getNumPages()):
                    pg=pread.getPage(page)
                    txt=pg.extractText()
                    s=s+txt

                # print(s)
                # list = []
                # list.append(str)
                # if search in s:
                #     print("here")
                #     return render(request, "search_page.html", {'lists':list})

                s=s.lower()
                search=search.lower()
                val = SequenceMatcher(None, search, s).ratio()
                pdf[val] = str

            x = sorted(pdf)
            list = []
            if len(x)<10:
                x.reverse()
                for i in x:
                    list.append(pdf[i].name[6:])
            return render(request, "search_page.html", {'lists':list})


    return render(request, "search_page.html", d)

#Method for admin notification
def A_notification(request):
    Notify = reversed(Notification.objects.filter(user_g_id=0).all())
    args = {'Notification' : Notify}

    #Code for deleting notification

    return render(request, "A_notification.html", args)

#A method for a repository option to view all repositories in admin page
###Not Implemented.###
def A_repository(request):
    return render(request, "A_repository.html")
