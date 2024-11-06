from django.contrib import admin
from django.urls import path
from adminapp import views

urlpatterns = [
    
    path('ObtainUserAuthToken',views.ObtainUserAuthToken.as_view(),name = 'ObtainUserAuthToken'),
    path('ObtainCustomerAuthToken',views.ObtainCustomerAuthToken.as_view(),name='ObtainCustomerAuthToken'),
    path('CustomerGet',views.CustomerGet.as_view(),name='CustomerGet'),

    path('GroupCreteApi',views.GroupCreteApi.as_view(),name='GroupCreteApi'),
   
    path('AllGetGroup',views.AllGetGroup.as_view(),name='AllGetGroup'),
    path('BlogCreateApi',views.BlogCreateApi.as_view(),name='BlogCreateApi'),
    path('upload-excel/', views.ExcelToDatabaseView, name='upload-excel'),
    
    # path('GetAccessToken', views.GetAccessToken.as_view(), name='GetAccessToken'),
    
    # path('FetchAllCountriesView', views.FetchAllCountriesView, name='FetchAllCountriesView'),

    # path('CheckTokenValidityView', views.CheckTokenValidityView, name='CheckTokenValidityView'),

    path('get_countries_data',views.get_countries_data,name='get_countries_data'),
    path('get_country_by_city/<str:city_name>/', views.get_country_by_city, name='get_country_by_city'),


    path('get_countries_data_code',views.get_countries_data_code,name='get_countries_data_code'),
    path('get_country_by_city_country_code', views.get_country_by_city_country_code, name='get_country_by_city_country_code'),
    path('search_country_by_city', views.search_country_by_city, name='search_country_by_city'),


    path('category/list',views.CategoryList.as_view(),name='category_list'),
    path('category/details/<int:id>',views.CategoryDetailes.as_view(),name='category_details'),


    path('faq/list',views.FAQList.as_view(),name='faq_list'),
    path('faq/details/<int:id>',views.FAQDetails.as_view(),name='faq_details'),

]