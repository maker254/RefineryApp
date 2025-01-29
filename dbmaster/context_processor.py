from .models import NavMainMenu,NavSubMenu
from django.template.defaulttags import register

def menulist(request):
   Masterquery =NavMainMenu.objects.filter(active=1).order_by('position') 
   returnArr={}
   submenulist=[]
   for details in Masterquery:
       submenulist=list(NavSubMenu.objects.filter(navmainmenu_id=details.id,active=1).values('url','application_name','sub_menu_name').order_by('position'))
       submenulist.append(details.icon)
       returnArr[details] =submenulist
   return {   
      "menulist": returnArr
   }