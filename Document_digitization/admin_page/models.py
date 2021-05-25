from django.db import models

#Group Model
class User_Group(models.Model):
    id = models.IntegerField(primary_key='True')
    group_name = models.CharField(max_length=30)
    creator = models.CharField(max_length=30)
    total_members = models.CharField(max_length=30, default = 0, null=True)

    def __str__(self):
        return str(self.id)

#Role Model
class User_Role(models.Model):
    id = models.IntegerField(primary_key='True')
    role = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id)


# User Model
class Plan_User(models.Model):
    id = models.IntegerField(primary_key='True')
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=20)
    userlink = models.URLField(max_length=50, blank=True)
    isactive = models.BooleanField(default=False)
    #group_id = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    group_id = models.ForeignKey(User_Group, on_delete=models.CASCADE, db_column="group_id", blank=True, null=False)
    role_id = models.ForeignKey(User_Role, on_delete=models.CASCADE, db_column="role_id")
    avatar = models.IntegerField(default=10)

    def __str__(self):
        return str(self.id)


#File
class Doc_Files(models.Model):
    name = models.CharField(max_length=30)
    doc = models.FileField(upload_to='Files/')
    upload_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(Plan_User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(User_Group, on_delete=models.CASCADE)

def __str__(self):
    return str(self.name)

# Avatar
class avatar(models.Model):
    id = models.IntegerField(primary_key='True')
    name = models.ImageField(upload_to = 'Avatar/')

    def __str__(self):
        return str(self.id)

#Notification Model
class Notification(models.Model):
    message = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField(Plan_User)
    user_g_id = models.IntegerField(default=0)

    def __str__(self):
        return self.message
