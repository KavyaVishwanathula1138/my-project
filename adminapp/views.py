from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .authentication import CustomTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import User, Customer,UserToken,CustomerToken,Blog,Category,FAQ
from .serializers import UserSerializer,CustomerSerializer,PermissionSerializer,CategorySerializer,GetCategorySerializer,FAQserrializer,GetFAQserializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from .authentication import CustomTokenAuthentication
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.http import Http404, JsonResponse, HttpResponse,FileResponse
from rest_framework import status

class ObtainUserAuthToken(APIView):
    def post(self, request, *args, **kwargs):        
        serializer = UserSerializer(data=request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        if serializer.is_valid():
            data = serializer.save()
            user = User.objects.get(id=data.id)
            token, created = UserToken.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'success':False,'error':serializer.errors})
   

class ObtainCustomerAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            customer = Customer.objects.get(id= data.id)
            token, created = CustomerToken.objects.get_or_create(user=customer)
            return Response({'token': token.key})
        else:
            return Response({'success':False,'error':serializer.errors})

class CustomerGet(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user

        if isinstance(user, Customer):
            if not user.has_perm('adminapp.view_customer'):
                return Response({'success': False, 'message': 'Permission denied customer'}, status=403)
        elif isinstance(user, User):
            if not user.has_perm('adminapp.view_customer'):
                return Response({'success': False, 'message': 'Permission denied user'}, status=403)

        return Response({'success': True, 'message': 'Hello Customer'})



class GroupCreteApi(APIView):
    def post(self, request):
        name = request.data.get('name')

        group_ins = Group.objects.create(name = name)
        return JsonResponse({'success':True,'message':'group creataed successfully'})

class AllGetGroup(APIView):
    def get(self, request):
        groups = Group.objects.all().order_by('-id')
        print(groups, 'data')

        all_permissions = []
        for group in groups:
            print(group,'group')
            permissions = group.permissions.all()
            print(permissions,'permissions')
            serializer = PermissionSerializer(permissions, many=True)
            all_permissions.extend(serializer.data)

        return JsonResponse({'data':all_permissions})


class UpdateGroupName(APIView):
    def put(self, request):
        group_id = request.data.get('group_id')
        name = request.data.get('name')
        try:
            grp_ins = Group.objects.get(id = group_id)

        except:
            return JsonResponse({'success':False})
        grp_ins.name = name
        grp_ins.save(update_fields=['name'])
        return JsonResponse({'success':True,'data':'updated successfully'})
      
class DeleteGroupName(APIView):
    def delete(self, request):
        group_id = request.data.get('group_id')
        try:
            grp_ins = Group.objects.get(id = group_id).delete()
            return JsonResponse({'success':True,'message':'deleted successfully'})
        except:
            return JsonResponse({'success':False})



class AllGetPermissions(APIView):
    def get(self, request):
        permissions = Permission.objects.all().order_by('id')
        serializer = PermissionSerializer(permissions, many=True)
        return JsonResponse({'success':True,'data':serializer.data})


class AddPermissionsToRole(APIView):
    def post(self, request):
        group_id = request.data.get('group_id')
        permission_ids = request.data.get('permission_ids')
        try:
            grp_ins = Group.objects.get(id=group_id)
        except:
            return JsonResponse({'success':False})
        for i in permission_ids:
            permissions = Permission.objects.get(id= i)
            grp_ins.permissions.add(permissions)

        return JsonResponse({'success':True})

class UpdatePermissionsToRole(APIView):
    def put(self, request):
        group_id = request.data.get('group_id')
        permission_ids = request.data.get('permission_ids')
        try:
            grp_ins = Group.objects.get(id=group_id)
        except:
            return JsonResponse({'success':False})
        grp_ins.permissions.clear()
        permissions_to_add = Permission.objects.filter(id__in=permission_ids)
        grp_ins.permissions.add(*permissions_to_add)

        return JsonResponse({'success':True})


class BlogCreateApi(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        if not request.user.has_perm('adminapp.add_blog'):
            return JsonResponse({'error': 'You do not have permission to access this resource.'})

        content = request.data.get('content')
        title = request.data.get('title')

        faq_ins = Blog.objects.create(content=content,title=title)
        return JsonResponse({'success':True})

class AllGetBlog(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        if not request.user.has_perm('adminapp.view_blog'):
            return JsonResponse({'error': 'You do not have permission to access this resource.'})

        data = list(Blog.objects.all().values())
        return JsonResponse({'success':True,'data':data})


# import pandas as pd
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Country
# from zipfile import BadZipFile


# @api_view(['POST'])
# def ExcelToDatabaseView(request):
#     if request.method == 'POST':
#         excel_file = request.FILES.get('excel_file')

#         if not excel_file:
#             return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Check if the file is a valid Excel format
#             file_name = excel_file.name
#             file_extension = file_name.split('.')[-1].lower()
#             if file_extension not in ['xlsx', 'xls']:
#                 return Response({'message': 'Unsupported file format. Please upload a .xlsx or .xls file.'}, status=status.HTTP_400_BAD_REQUEST)

#             # Read Excel data
#             if file_extension == 'xlsx':
#                 excel_data = pd.read_excel(excel_file, engine='openpyxl')
#             elif file_extension == 'xls':
#                 excel_data = pd.read_excel(excel_file, engine='xlrd')

#             # Clean column names by stripping spaces
#             excel_data.columns = excel_data.columns.str.strip()

#             # Check for required columns
#             expected_columns = ['Country', 'Country code', 'International dialing']
#             if not all(col in excel_data.columns for col in expected_columns):
#                 missing_columns = [col for col in expected_columns if col not in excel_data.columns]
#                 return Response({'message': f'Required columns missing in Excel file: {missing_columns}'}, status=status.HTTP_400_BAD_REQUEST)

#             try:
#                 insert_data_to_db(excel_data)
#             except Exception as e:
#                 print(f"An unexpected error occurred during database insertion: {str(e)}")
#                 return Response({'message': 'An unexpected error occurred.'}, status=status.HTTP_400_BAD_REQUEST)

#             return Response({'message': 'Data imported successfully'})

#         except:
#             return Response({'message': 'Data Cannot  Be Imported '}, status=status.HTTP_400_BAD_REQUEST)


# def insert_data_to_db(excel_data):
#     for index, row in excel_data.iterrows():
#         country_name = row['Country']
#         short_form = row['Country code']
#         international_dialing = row['International dialing']

#         print(f"Inserting row {index + 1}: {country_name}, {short_form}, {international_dialing}")

#         Country.objects.create(
#             country_name=country_name,
#             short_form=short_form,
#             international_dialing=international_dialing
#         )


# from rest_framework.decorators import api_view
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import requests

# @api_view(['GET'])
# @csrf_exempt
# def ExcelToDatabaseView(request):
#     if request.method == 'GET':
#         city_name = request.query_params.get('city_name')

#         if not city_name:
#             return JsonResponse({'error': 'City name parameter is missing'}, status=400)

#         # Step 1: Get country code from api.api-ninjas.com
#         api_url = f'https://api.api-ninjas.com/v1/city?name={city_name}'
#         headers = {'X-Api-Key': 'PGWmvaBfdu9B4LxL6Ftiow==LWYrQdlVYaTdeIOB'}

#         try:
#             response = requests.get(api_url, headers=headers)
#             if response.status_code == requests.codes.ok:
#                 data = response.json()

#                 if isinstance(data, list):
#                     if data:
#                         country_code = data[0].get('country', '')
#                     else:
#                         country_code = ''
#                 elif isinstance(data, dict):
#                     country_code = data.get('country', '')
#                 else:
#                     country_code = ''

#                 # Step 2: Get full country name from restcountries.com
#                 if country_code:
#                     restcountries_url = f'https://restcountries.com/v3.1/alpha/{country_code}'
#                     restcountries_response = requests.get(restcountries_url)

#                     if restcountries_response.status_code == requests.codes.ok:
#                         country_data = restcountries_response.json()

#                         # Extract common name from the detailed country_data
#                         if isinstance(country_data, list):
#                             # Handle case where country_data is a list
#                             if country_data:
#                                 country_name = country_data[0].get('name', {}).get('common', '')
#                             else:
#                                 country_name = ''
#                         elif isinstance(country_data, dict):
#                             # Handle case where country_data is a dictionary
#                             country_name = country_data.get('name', {}).get('common', '')
#                         else:
#                             country_name = ''

#                         return JsonResponse({'success': True, 'country_name': country_name})
#                     else:
#                         return JsonResponse({'success': False, 'message': 'Failed to fetch country data'}, status=500)
#                 else:
#                     return JsonResponse({'success': False, 'message': 'No country code found for the city'}, status=404)
#             else:
#                 return JsonResponse({'success': False, 'message': 'Failed to fetch city data'}, status=500)
#         except requests.exceptions.RequestException as e:
#             return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)


#######################################################
# from rest_framework.decorators import api_view
# from django.http import JsonResponse
# import requests

# @api_view(['GET'])
# def ExcelToDatabaseView(request):
#     city_name = request.query_params.get('city_name')

#     if not city_name:
#         return JsonResponse({'error': 'City name parameter is missing'}, status=400)

#     try:
#         # Step 1: Get city details from api.api-ninjas.com based on first three letters of city_name
#         api_url = f'https://api.api-ninjas.com/v1/city?name__startswith={city_name[:3]}'
#         headers = {'X-Api-Key': 'PGWmvaBfdu9B4LxL6Ftiow==LWYrQdlVYaTdeIOB'}
#         response = requests.get(api_url, headers=headers)
#         response.raise_for_status()  # Raise exception for non-200 status codes

#         city_data = response.json()

#         # Step 2: Extract unique country codes for all entries where city_name matches
#         country_codes = set()  # Use a set to ensure unique country codes
#         for entry in city_data:
#             country_code = entry.get('country', '')
#             if country_code:
#                 country_codes.add(country_code)

#         # Step 3: Get full country names from restcountries.com using country codes
#         country_names = []
#         for country_code in country_codes:
#             restcountries_url = f'https://restcountries.com/v3.1/alpha/{country_code}'
#             restcountries_response = requests.get(restcountries_url)
#             restcountries_response.raise_for_status()

#             country_data = restcountries_response.json()

#             if isinstance(country_data, list):
#                 # Handle case where country_data is a list (unexpected for restcountries.com)
#                 for entry in country_data:
#                     common_name = entry.get('name', {}).get('common', '')
#                     if common_name and common_name not in country_names:
#                         country_names.append(common_name)
#             elif isinstance(country_data, dict):
#                 # Handle case where country_data is a dictionary
#                 common_name = country_data.get('name', {}).get('common', '')
#                 if common_name and common_name not in country_names:
#                     country_names.append(common_name)

#         if country_names:
#             return JsonResponse({'success': True, 'country_names': country_names})
#         else:
#             return JsonResponse({'success': False, 'message': f'No countries found for the city {city_name}'}, status=404)

#     except requests.exceptions.RequestException as e:
#         return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)


####################################################

# from rest_framework.decorators import api_view
# from django.http import JsonResponse
# import requests

# @api_view(['GET'])
# def ExcelToDatabaseView(request):
#     city_name = request.query_params.get('city_name')

#     if not city_name:
#         return JsonResponse({'error': 'City name parameter is missing'}, status=400)

#     try:
#         # Step 1: Get city details from api.api-ninjas.com name__startswith={city_name[:3]}
#         api_url = f'https://api.api-ninjas.com/v1/city?name__startswith={city_name[:3]}'
#         headers = {'X-Api-Key': 'PGWmvaBfdu9B4LxL6Ftiow==LWYrQdlVYaTdeIOB'}
#         response = requests.get(api_url, headers=headers)
#         response.raise_for_status()  # Raise exception for non-200 status codes

#         city_data = response.json()

#         # Step 2: Extract unique country codes for all entries where city_name matches
#         country_codes = set()  # Use a set to ensure unique country codes
#         for entry in city_data:
#             country_code = entry.get('country', '')
#             if country_code:
#                 country_codes.add(country_code)

#         # Step 3: Get full country names from restcountries.com using country codes
#         country_names = []
#         for country_code in country_codes:
#             restcountries_url = f'https://restcountries.com/v3.1/alpha/{country_code}'
#             restcountries_response = requests.get(restcountries_url)
#             restcountries_response.raise_for_status()

#             country_data = restcountries_response.json()

#             if isinstance(country_data, list):
#                 # Handle case where country_data is a list (unexpected for restcountries.com)
#                 for entry in country_data:
#                     common_name = entry.get('name', {}).get('common', '')
#                     if common_name and common_name not in country_names:
#                         country_names.append(common_name)
#             elif isinstance(country_data, dict):
#                 # Handle case where country_data is a dictionary
#                 common_name = country_data.get('name', {}).get('common', '')
#                 if common_name and common_name not in country_names:
#                     country_names.append(common_name)

#         if country_names:
#             return JsonResponse({'success': True, 'country_names': country_names})
#         else:
#             return JsonResponse({'success': False, 'message': f'No countries found for the city {city_name}'}, status=404)

#     except requests.exceptions.RequestException as e:
#         return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)



#######################################################3333






# class GetAccessToken(APIView):
#     def get(self, request):
#         api_token = 'N2vDOagLh20v1gDkIjFY0fT_mpf70FrZVY6-WjUZm2LTZkJNIQG_LZvqPb5KPUG6zZ4'
#         user_email = 'kavyavishwanathula123@gmail.com'
        
#         url = 'https://www.universal-tutorial.com/api/getaccesstoken'
#         headers = {
#             'Accept': 'application/json',
#             'api-token': api_token,
#             'user-email': user_email
#         }
        
#         response = requests.get(url, headers=headers)
        
#         if response.status_code == 200:
#             return response.json()['auth_token']
#         else:
#             print(f"Failed to get access token. Status code: {response.status_code}, Response: {response.content}")
#             return None


# from rest_framework.decorators import api_view
# from django.http import JsonResponse
# import requests

# @api_view(['GET'])
# def FetchAllCountriesView(request):
#     try:
#         # Endpoint to fetch all countries data
#         api_url = 'https://www.universal-tutorial.com/api/countries/'
#         headers = {
#             "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJfZW1haWwiOiJrYXZ5YXZpc2h3YW5hdGh1bGExMjNAZ21haWwuY29tIiwiYXBpX3Rva2VuIjoiTjJ2RE9hZ0xoMjB2MWdEa0lqRlkwZlRfbXBmNzBGclpWWTYtV2pVWm0yTFRaa0pOSVFHX0xadnFQYjVLUFVHNnpaNCJ9LCJleHAiOjE3MTkzMTIzMzF9.DNbsSnv9_ldETHYBjEJzIh4mlOu65G04nHlDBXIC0u4",  # Replace with your actual access token
#             "Accept": "application/json"
#         }

#         print(f"Requesting all countries data from {api_url}")
#         response = requests.get(api_url, headers=headers)
#         print(f"Response status code: {response.status_code}")

#         # Check if the response is successful (status code 200)
#         if response.status_code == 200:
#             all_countries_data = response.json()
#             print(f"All countries data received: {all_countries_data}")
#             return JsonResponse({'success': True, 'data': all_countries_data})
#         else:
#             # Handle unexpected status codes
#             error_message = f"Error: Unexpected status code {response.status_code} - {response.content}"
#             print(error_message)
#             return JsonResponse({'success': False, 'message': error_message}, status=response.status_code)

#     except requests.exceptions.RequestException as e:
#         # Handle request exceptions
#         error_message = f"Error: {str(e)}"
#         print(error_message)
#         return JsonResponse({'success': False, 'message': error_message}, status=500)

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import requests

# @api_view(['GET'])
# def ExcelToDatabaseView(request):
#     city_name = request.query_params.get('city_name')

#     if not city_name:
#         print('City name parameter is missing')
#         return Response({'error': 'City name parameter is missing'}, status=400)

#     try:
#         # Step 1: Get access token
#         print('Getting access token...')
#         access_token = GetAccessToken().get(request)
#         if not access_token:
#             print('Failed to get access token')
#             return Response({'success': False, 'message': 'Failed to get access token'}, status=500)

#         # Step 2: Get city details based on city_name
#         cities_url = f'https://www.universal-tutorial.com/api/cities/'
#         print(f'Requesting cities data for city {city_name}...')
#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Accept": "application/json"
#         }

#         response = requests.get(cities_url, params={'search': city_name}, headers=headers)
#         print(f'Response status code: {response.status_code}')

#         if response.status_code == 200:
#             cities_data = response.json()
#             print(f'All cities for "{city_name}": {cities_data}')

#             # Find the city with exact matching city_name
#             desired_city = None
#             for city in cities_data:
#                 if city['city_name'].lower() == city_name.lower():
#                     desired_city = city
#                     break

#             if not desired_city:
#                 print(f'City "{city_name}" not found')
#                 return Response({'success': False, 'message': f'City "{city_name}" not found'}, status=404)

#             # Step 3: Get country details for the desired city
#             country_id = desired_city.get('country_id')
#             if not country_id:
#                 print('Country ID not found for the city')
#                 return Response({'success': False, 'message': 'Country ID not found for the city'}, status=404)

#             country_url = f'https://www.universal-tutorial.com/api/countries/{country_id}'
#             print(f'Requesting country data for country ID {country_id}...')
#             response = requests.get(country_url, headers=headers)
#             print(f'Response status code: {response.status_code}')

#             if response.status_code == 200:
#                 country_data = response.json()
#                 country_name = country_data.get('country_name')
#                 if not country_name:
#                     print('Country not found for the city')
#                     return Response({'success': False, 'message': 'Country not found for the city'}, status=404)

#                 print(f'Country found for city "{city_name}": {country_name}')
#                 return Response({'success': True, 'country_name': country_name})

#             else:
#                 print('Failed to fetch country data')
#                 return Response({'success': False, 'message': 'Failed to fetch country data'}, status=response.status_code)

#         elif response.status_code == 404:
#             print(f'City "{city_name}" not found')
#             return Response({'success': False, 'message': f'City "{city_name}" not found'}, status=404)

#         else:
#             print(f'Failed to fetch city data. Status code: {response.status_code}')
#             return Response({'success': False, 'message': f'Failed to fetch city data. Status code: {response.status_code}'}, status=response.status_code)

#     except requests.exceptions.RequestException as e:
#         print(f'Error occurred: {str(e)}')
#         return Response({'success': False, 'message': f'Error: {str(e)}'}, status=500)



# from django.shortcuts import render
# from django_countries import countries

# def country_list(request):
#     all_countries = list(countries)
#     print(all_countries,'all_countries')
#     return JsonResponse({'success':True})

# from django.shortcuts import get_object_or_404
# from cities.models import City, Country
# from django.http import JsonResponse

# def get_countries_by_city_name(request):
#     city_name = request.GET.get("city_name")
#     print(f"City Name from request: {city_name}")

#     if city_name:
#         # Query for cities with matching names
#         cities = City.objects.filter(name__icontains=city_name)
#         print(f"Matching Cities Query: {cities.query}")

#         # Initialize an empty list to store unique country IDs
#         country_ids = []

#         # Iterate over matching cities to collect unique country IDs
#         for city in cities:
#             if city.country_id not in country_ids:
#                 country_ids.append(city.country_id)

#         print(f"Unique Country IDs: {country_ids}")

#         if not country_ids:
#             # Handle case where no cities were found for the given name
#             return JsonResponse({"error": "No cities found for the given name."}, status=404)

#         # Retrieve countries based on the collected country IDs
#         countries = Country.objects.filter(id__in=country_ids).order_by('name')
#         print(f"Countries Query: {countries.query}")

#         return countries
#     else:
#         # Handle case where city_name parameter is missing or empty
#         return JsonResponse({"error": "City name parameter is missing or empty."}, status=400)




from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests

@api_view(['GET'])
def ExcelToDatabaseView(request):
    city_name = request.query_params.get('city_name')

    if not city_name:
        return JsonResponse({'error': 'City name parameter is missing'}, status=400)

    try:
        # Step 1: Get city details from api.api-ninjas.com name__startswith={city_name[:3]}
        api_url = f'https://api.api-ninjas.com/v1/city?name__startswith={city_name[:3]}'
        headers = {'X-Api-Key': 'PGWmvaBfdu9B4LxL6Ftiow==LWYrQdlVYaTdeIOB'}
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise exception for non-200 status codes

        city_data = response.json()

        # Step 2: Extract unique country codes for all entries where city_name matches
        country_codes = set()  # Use a set to ensure unique country codes
        for entry in city_data:
            country_code = entry.get('country', '')
            if country_code:
                country_codes.add(country_code)

        # Step 3: Get full country names from restcountries.com using country codes
        country_names = []
        for country_code in country_codes:
            restcountries_url = f'https://restcountries.com/v3.1/alpha/{country_code}'
            restcountries_response = requests.get(restcountries_url)
            restcountries_response.raise_for_status()

            country_data = restcountries_response.json()

            if isinstance(country_data, list):
                # Handle case where country_data is a list (unexpected for restcountries.com)
                for entry in country_data:
                    common_name = entry.get('name', {}).get('common', '')
                    if common_name and common_name not in country_names:
                        country_names.append(common_name)
            elif isinstance(country_data, dict):
                # Handle case where country_data is a dictionary
                common_name = country_data.get('name', {}).get('common', '')
                if common_name and common_name not in country_names:
                    country_names.append(common_name)

        if country_names:
            return JsonResponse({'success': True, 'country_names': country_names})
        else:
            return JsonResponse({'success': False, 'message': f'No countries found for the city {city_name}'}, status=404)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)


##################################################################
# import requests
# from django.http import JsonResponse, HttpResponse

# countries_data = None

# def get_countries_data(request):
#     global countries_data
#     url = "https://countriesnow.space/api/v0.1/countries"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  
#         countries_data = response.json() 
#         print("Countries data loaded successfully") 
#         return JsonResponse(countries_data)
#     except (requests.exceptions.HTTPError, 
#             requests.exceptions.ConnectionError, 
#             requests.exceptions.Timeout, 
#             requests.exceptions.RequestException) as err:
#         print(f"An error occurred: {err}")  # Debug print
#         return JsonResponse({'error': f"Failed to load countries data: {str(err)}"}, status=500)

# def get_country_by_city(request, city_name):
#     global countries_data
    
#     if not countries_data:
#         countries_response = get_countries_data(request)
#         if countries_response.status_code != 200:
#             return countries_response  
#         countries_data = countries_response.json() 
    
#     matching_countries = []
#     for country in countries_data.get('data', []):
#         if city_name in country.get('cities', []):
#             matching_countries.append(country['country'])
    
#     if matching_countries:
#         print(f"Matching countries found: {matching_countries}") 
#         return JsonResponse({'countries': matching_countries})
    
#     print(f"No country found for city: {city_name}")  # Debug print
#     return JsonResponse({'message': f"No country found for city: {city_name}"}, status=404)

###############################################################
# import requests
# from django.http import JsonResponse, HttpResponse

# countries_data = None

# def get_countries_data():
#     global countries_data
#     url = "https://countriesnow.space/api/v0.1/countries"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  
#         countries_data = response.json()['data']  # Store only the 'data' part of the response
#         print("Countries data loaded successfully") 
#     except (requests.exceptions.HTTPError, 
#             requests.exceptions.ConnectionError, 
#             requests.exceptions.Timeout, 
#             requests.exceptions.RequestException) as err:
#         print(f"An error occurred: {err}")  # Debug print
#         countries_data = []  # Initialize as empty list in case of error

# def get_country_by_city(request, city_name):
#     global countries_data
    
#     if countries_data is None:
#         get_countries_data()  # Ensure countries_data is populated
    
#     matching_countries = []
    
#     # Check if the city_name matches any country name directly or is in the cities list
#     for country in countries_data:
#         if city_name == country['country']:  # Check if city_name is the country name
#             matching_countries.append(country['country'])
#         elif city_name in country.get('cities', []):
#             matching_countries.append(country['country'])
    
#     if matching_countries:
#         print(f"Matching countries found: {matching_countries}") 
#         return JsonResponse({'countries': matching_countries})
    
#     print(f"No country found for city: {city_name}")  # Debug print
#     return JsonResponse({'message': f"No country found for city: {city_name}"}, status=404)


######################################################
##########################################

# # ***************************************************************
import requests
from django.http import JsonResponse

countries_data = None

def get_countries_data():
    global countries_data
    url = "https://countriesnow.space/api/v0.1/countries"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        countries_data = response.json()['data']  
        print("Countries data loaded successfully") 
    except (requests.exceptions.HTTPError, 
            requests.exceptions.ConnectionError, 
            requests.exceptions.Timeout, 
            requests.exceptions.RequestException) as err:
        print(f"An error occurred: {err}")  
        countries_data = [] 

def get_country_by_city(request, city_name):
    global countries_data
    
    if countries_data is None:
        get_countries_data() 
    
    matching_entries = []

    city_name_lower = city_name.lower()

    # Iterate through countries_data to find matches
    for country in countries_data:
        country_name_lower = country['country'].lower()
        cities = country.get('cities', [])

        # Check if city_name_lower matches country_name_lower from the start
        if country_name_lower.startswith(city_name_lower):
            matching_entries.append({'country': country['country']})

        # Check if city_name_lower matches any city name from the start
        matched_cities = [city for city in cities if city.lower().startswith(city_name_lower)]
        if matched_cities:
            matching_entries.append({'country': country['country'], 'cities': matched_cities})

    if matching_entries:
        print(f"Matching entries found: {matching_entries}") 
        return JsonResponse({'matching_entries': matching_entries})
    
    print(f"No matches found for city: {city_name}")  # Debug print
    return JsonResponse({'message': f"No matches found for city: {city_name}"}, status=404)







# import requests
# from django.http import JsonResponse

# countries_data = None

# def get_countries_data():
#     global countries_data
#     url = "https://countriesnow.space/api/v0.1/countries"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         countries_data = response.json()['data']  # Store only the 'data' part of the response
#         print("Countries data loaded successfully") 
#     except (requests.exceptions.HTTPError, 
#             requests.exceptions.ConnectionError, 
#             requests.exceptions.Timeout, 
#             requests.exceptions.RequestException) as err:
#         print(f"An error occurred: {err}")  # Debug print
#         countries_data = []  # Initialize as empty list in case of error

# def get_country_by_city(request, city_name):
#     global countries_data
    
#     if countries_data is None:
#         get_countries_data() 
    
#     matching_entries = []

#     if len(city_name) >= 3:
#         city_name_lower = city_name.lower()
#         # Check if city_name matches any country name directly or is in the cities list
#         for country in countries_data:
#             if city_name_lower == country['country'].lower():  # Check if city_name matches the country name
#                 matching_entries.append({'country': country['country']})
#             else:
#                 matched_cities = [city for city in country.get('cities', []) if city_name_lower in city.lower()]
#                 if matched_cities:
#                     matching_entries.append({'country': country['country'], 'cities': matched_cities})

#     else:
#         print("Please enter at least 3 characters for city search.")  # Debug print
#         return JsonResponse({'message': "Please enter at least 3 characters for city search."}, status=400)
    
#     if matching_entries:
#         print(f"Matching entries found: {matching_entries}") 
#         return JsonResponse({'matching_entries': matching_entries})
    
#     print(f"No matches found for city: {city_name}")  # Debug print
#     return JsonResponse({'message': f"No matches found for city: {city_name}"}, status=404)


###************************************************************
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

countries_dataa = None

def get_countries_data_code():
    global countries_dataa
    url = "https://countriesnow.space/api/v0.1/countries"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        countries_dataa = response.json()['data']  # Store only the 'data' part of the response
        print("Countries data loaded successfully") 
    except (requests.exceptions.HTTPError, 
            requests.exceptions.ConnectionError, 
            requests.exceptions.Timeout, 
            requests.exceptions.RequestException) as err:
        print(f"An error occurred: {err}")  # Debug print
        countries_dataa = []  # Initialize as empty list in case of error

def get_country_by_city_country_code(request, searchparam):
    global countries_dataa
    
    if countries_dataa is None:
        get_countries_data_code()  
    
    matching_entries = []

    searchparam_lower = searchparam.lower()

    if len(searchparam_lower) >= 3:
        # Iterate through countries_dataa to find matches
        for country in countries_dataa:
            country_name_lower = country['country'].lower()
            country_code = country.get('country_code', '')  # Get country_code with default empty string
            iso2 = country.get('iso2', '').lower()  # Get ISO2 code with default empty string and convert to lowercase
            iso3 = country.get('iso3', '').lower()  # Get ISO3 code with default empty string and convert to lowercase
            cities = country.get('cities', [])

            # Check if searchparam_lower matches country name, country code, ISO2, ISO3, or any city name
            if (searchparam_lower in country_name_lower or
                searchparam_lower == country_code or
                searchparam_lower == iso2 or
                searchparam_lower == iso3 or
                any(city.lower().startswith(searchparam_lower) for city in cities)):
                
                # If searchparam_lower matches country name exactly
                if searchparam_lower == country_name_lower:
                    matching_entries.append({
                        'country': country['country'],
                        'country_code': country_code,
                        'iso2': iso2.upper(),  # Return ISO2 in uppercase
                        'iso3': iso3.upper()   # Return ISO3 in uppercase
                    })
                else:
                    # Check if searchparam_lower is in any city name (starts with)
                    matched_cities = [city for city in cities if city.lower().startswith(searchparam_lower)]
                    if matched_cities:
                        matching_entries.append({
                            'country': country['country'],
                            'country_code': country_code,
                            'iso2': iso2.upper(),  # Return ISO2 in uppercase
                            'iso3': iso3.upper(),  # Return ISO3 in uppercase
                            'cities': matched_cities
                        })

    else:
        print(f"Search parameter '{searchparam}' does not meet the minimum length requirement.")  # Debug print
        return JsonResponse({'message': f"Search parameter '{searchparam}' does not meet the minimum length requirement."}, status=400)
    
    if matching_entries:
        print(f"Matching entries found: {matching_entries}") 
        return JsonResponse({'matching_entries': matching_entries})
    
    print(f"No matches found for search parameter: {searchparam}")  # Debug print
    return JsonResponse({'message': f"No matches found for search parameter: {searchparam}"}, status=404)

@csrf_exempt
@require_http_methods(["GET"])  # Adjust HTTP methods as needed
def search_country_by_city(request):
    searchparam = request.GET.get('searchparam', '')
    print(f"Received search parameter: {searchparam}")  # Debug print
    
    if not searchparam:
        print("Search parameter 'searchparam' is required.")  # Debug print
        return JsonResponse({'message': "Search parameter 'searchparam' is required."}, status=400)
    
    return get_country_by_city_country_code(request, searchparam)


from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
import uuid
from django.core.files.base import ContentFile

def decode_base64_file(data):
    format, imgstr = data.split(';base64,') 
    ext = format.split('/')[-1] 
    id = uuid.uuid4()
    return ContentFile(base64.b64decode(imgstr), name=f'{id}.{ext}')


class CategoryList(APIView):
    parser_classes = [JSONParser]

    def get(self, request, format=None):
        category_ins = Category.objects.all().order_by('-id')
        serializer = GetCategorySerializer(category_ins, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        category_image = request.data.get('category_image')
        if category_image and 'base64' in category_image:
            request.data['category_image'] = decode_base64_file(category_image)
        serializer = CategorySerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailes(APIView):
    def get_object(self,id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise Http404

    def get(self,request,id,format=None):
        task = self.get_object(id)
        serializer = GetCategorySerializer(task)
        return Response(serializer.data)
        
    def put(self, request, id, format=None):
        task = self.get_object(id)
        category_image = request.data.get('category_image')
        if category_image and 'base64' in category_image:
            request.data['category_image'] = decode_base64_file(category_image)
        serializer = CategorySerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            
            data = serializer.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,format=None):
        port_ins=self.get_object(id)
        port_ins.status=False
        port_ins.save()
        return Response({"success":True,"data":"Category Deleted Successfully"})


class FAQList(APIView):
    def get(self, request, format=None):
        task = FAQ.objects.all()
        serializer = GetFAQserializer(task, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer=FAQserrializer(data=request.data,partial=True)
        if serializer.is_valid():

            data=serializer.save(created_by = request.user.id)
           

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FAQDetails(APIView):
    def get_object(self, id):
        try:
            return FAQ.objects.get(id=id)
        except FAQ.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        task = self.get_object(id)
        serializer = GetFAQserializer(task)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        task = self.get_object(id)
        serializer = FAQserrializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            data = serializer.save(modified_by=request.user.id)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        ins = self.get_object(id)
        ins.delete()
        return JsonResponse({'success': True, 'data': 'Successfully Deleted record'})  
