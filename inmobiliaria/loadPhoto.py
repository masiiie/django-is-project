from administracion.models import PageImage

def load():
    try:
       img=PageImage.objects.all()[0]        
    except Exception:
       img=''
    return img
