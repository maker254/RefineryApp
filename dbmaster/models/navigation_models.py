from django.db import models
import datetime

class NavMainMenu(models.Model):
    menu_name =models.CharField('Menu Name',max_length=100,unique=True)
    menu_id=models.CharField('Menu ID',max_length=100,default='')
    icon = models.CharField('Icon Name',max_length=100,default='')
    position =models.IntegerField(default=0)
    active=models.BooleanField('Active',default =True)
    class Meta:
              verbose_name_plural="Main_menu"
    def __str__(self):
        return str(self.menu_name)

class  NavSubMenu(models.Model):
    sub_menu_name = models.CharField('Submenu Name',max_length=100)
    application_name=models.CharField('App Name',max_length = 50,default='')
    url = models.CharField('Url',max_length=100,default='#')
    position =models.IntegerField(default=0)
    active=models.BooleanField('Active',default =True)
    navmainmenu=models.ForeignKey('NavMainMenu', on_delete = models.PROTECT)
    class Meta:
              verbose_name_plural="Sub_menu"

    def __str__(self):
            return str(self.sub_menu_name)
            
def navigate_model(nav_btn_data,data_model):
     if nav_btn_data['nav-button']=='first':
               query=data_model.objects.order_by('id').first()
               if query:
                    return query.id
               else:
                    return None
     elif nav_btn_data['nav-button'] =='forward':
               if nav_btn_data['id']:
                         query=data_model.objects.filter(id__gt=nav_btn_data['id']).order_by('id').first()
                         if query:
                              return query.id
                         else:
                              query=data_model.objects.order_by('id').first()
                              return query.id
               else :
                    query=data_model.objects.order_by('id').first()
                    if query:
                              return query.id
                    else:
                              return None
     elif nav_btn_data['nav-button'] =='backward':
          if nav_btn_data['id']:
               query=data_model.objects.filter(id__lt=nav_btn_data['id']).order_by('id').last()
               if query:
                    return query.id
               else:
                    query=data_model.objects.order_by('id').last()
                    return query.id
          else:
               query=data_model.objects.order_by('id').last()
               if query:
                    return query.id
               else:
                    return None
     elif  nav_btn_data['nav-button']=='last':
               query=data_model.objects.order_by('id').last()
               if query:
                    return query.id
               else:
                    return None