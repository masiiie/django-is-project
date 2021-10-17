from .models import *

def initialize_keepcalm():
    initialize_groups()
    initialize_users()

def initialize_groups():
    q = Group.objects.create(name = "Administrador")
    # q.permissions = ['inmobiliaria.change_lugar',
    #                 'inmobiliaria.delete_cuarto', 
    #                 'inmobiliaria.delete_tag', 
    #                 'auth.change_user', 
    #                 'inmobiliaria.add_alquiler', 
    #                 'inmobiliaria.add_tag', 
    #                 'auth.add_user', 
    #                 'inmobiliaria.add_cuarto', 
    #                 'inmobiliaria.delete_lugar', 
    #                 'inmobiliaria.change_tag', 
    #                 'inmobiliaria.add_lugar', 
    #                 'inmobiliaria.change_cuarto', 
    #                 'inmobiliaria.change_alquiler', 
    #                 'inmobiliaria.delete_alquiler',
    #               # 'inmobiliaria.view_profile',]


    # q.permissions.set('inmobiliaria.change_lugar',
    #                  'inmobiliaria.delete_cuarto', 
    #                  'inmobiliaria.delete_tag', 
    #                  'auth.change_user', 
    #                  'inmobiliaria.add_alquiler', 
    #                  'inmobiliaria.add_tag', 
    #                  'auth.add_user', 
    #                  'inmobiliaria.add_cuarto', 
    #                  'inmobiliaria.delete_lugar', 
    #                  'inmobiliaria.change_tag', 
    #                  'inmobiliaria.add_lugar', 
    #                  'inmobiliaria.change_cuarto', 
    #                  'inmobiliaria.change_alquiler', 
    #                  'inmobiliaria.delete_alquiler',
                    # 'inmobiliaria.view_profile',
    #                  )

    q = Group.objects.create(name = "Perito")
    # q.permissions.set(['inmobiliaria.add_lugar', 
    #                 'inmobiliaria.add_cuarto', 
    #                 'inmobiliaria.add_tag',
                    # 'inmobiliaria.view_profile',
    #                 ])

    q = Group.objects.create(name = "Cliente")
    # q.permissions.set([inmobiliaria.view_profile'])

    q = Group.objects.create(name = "Visitante")
    # q.permissions.set([])


def initialize_users():
    User.objects.create_superuser("ernesto","ernestoestevanell@gmail.com","erne199609")

    q = User.objects.create_user("sandor",password = "s12345678",is_staff = True)
    groups = Group.objects.get(name = "Administrador")
    q.groups.add(groups)

    q = User.objects.create_user("zahuis",password = "z12345678",is_staff = True)
    groups = Group.objects.get(name = "Perito")
    q.groups.add(groups)

    q = User.objects.create_user("massiel",password = "m12345678")
    groups = Group.objects.get(name = "Visitante")
    q.groups.add(groups)

    q = User.objects.create_user("alejandro",password = "a12345678")
    groups = Group.objects.get(name = "Cliente")
    q.groups.add(groups)