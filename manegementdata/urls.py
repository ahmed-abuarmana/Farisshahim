from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.index, name="index"),
    
    path("makhabez/", views.makhabez_list, name="makhabez_list"),
    path("makhabez/<int:pk>/", views.makhabez_detail, name="makhabez_detail"),

    path("takiyat/", views.takiyat_list, name="takiyat_list"),
    path("takiyat/<int:pk>/", views.takiya_detail, name="takiya_detail"),

    path('makhbaz/<int:makhbaz_id>/add_tasleema/', views.add_tasleema_for_makhbaz, name='add_tasleema_for_makhbaz'),
    path('takiya/<int:takiya_id>/add_tasleema/', views.add_tasleema_for_takiya, name='add_tasleema_for_takiya'),

    path('makhabez/add/', views.add_new_makhbaz, name='add_new_makhbaz'),
    path('takiyat/add/', views.add_new_takiya, name='add_new_takiya'),

    path('makhabez/<int:makhbaz_id>/delete/', views.delete_makhbaz, name='delete_makhbaz'),
    path('takiyat/<int:takiya_id>/delete/', views.delete_takiya, name='delete_takiya'),

    path('makhabez/<int:pk>/update/', views.update_makhbaz, name='update_makhbaz'),
    path('takiyat/<int:pk>/update/', views.update_takiya, name='update_takiya'),

    path('makhabez/<int:makhbaz_id>/export_excel/', views.export_makhbaz_excel, name='export_makhbaz_excel'),
    path('takaya/<int:takiya_id>/export_excel/', views.export_takiya_excel, name='export_takiya_excel'),

    path('takiya/<int:takiya_id>/add-beneficiary/', views.add_beneficiary_for_takiya, name='add_beneficiary_for_takiya'),
    path('makhbaz/<int:makhbaz_id>/add-beneficiary/', views.add_beneficiary_for_makhbaz, name='add_beneficiary_for_makhbaz'),

    path('beneficiaries/takiya/', views.all_beneficiaries_takiya, name='all_beneficiaries_takiya'),
    path('beneficiaries/makhbaz/', views.all_beneficiaries_makhbaz, name='all_beneficiaries_makhbaz'),

    path("export_makhabez_excel/", views.export_makhabez_excel, name="export_makhabez_excel"),
    path("export_takiyat_excel/", views.export_takiyat_excel, name="export_takiyat_excel"),

]
