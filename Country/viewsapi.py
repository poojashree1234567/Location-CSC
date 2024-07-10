from django.views import View
from .models import Country, State, City
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
import json
from django.core.paginator import Paginator

#csrf token
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

#Create API for COuntry -> get, post, put, delete
class CountryApiView(View):
    def get(self, request):
        countryobj = Country.objects.all() #complex obj ---- python data hai to vo convert hota hai json me
        countrylist = []

        for item in countryobj:
            Countrydata = {}
            Countrydata['name'] = item.name
            Countrydata['slug'] = item.slug
            countrylist.append(Countrydata)

        print(countrylist)
        return JsonResponse(countrylist, safe=False )
    
    def post(self, request):
        country_name = request.POST.get('country_name')
        slug = request.POST.get('slug')
        code = request.POST.get('code')
        flag = request.FILES.get('flag')
        state_available = request.POST.get('state_available') == '1' #convert to boolean

        if not state_available:
            state_available=False

        if Country.objects.filter(code=code).exists():
            context = {'message': 'Country already exist'}
            return JsonResponse(context)
        
        if Country.objects.filter(slug=slug).exists():
            context = {'message': 'Slug already exist'}
            return JsonResponse(context)
        
        if Country.objects.filter(name=country_name).exists():
            context = {'message': 'Country created successfully'}           
            return JsonResponse(context)
        
        # If the country does not exist, create a new one
        Country.objects.create(
            name=country_name, 
            slug=slug, 
            code=code, 
            flag=flag, 
            is_state_available=state_available)
        
        context = {'message': 'Country created successfully'}
        return JsonResponse(context)
    
    def put(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

        slug = data.get('slug')
        if not slug:
            return JsonResponse({'message': 'Slug is required'}, status=400)

        try:
            countryobj = Country.objects.get(slug=slug)
        except Country.DoesNotExist:
            return JsonResponse({'message': 'Country not found'}, status=404)

        country_name = data.get('country_name')
        code = data.get('code')
        new_slug = data.get('new_slug')
        state_available = data.get('state_available')
        flag = request.FILES.get('flag')

        if country_name:
            countryobj.name = country_name

        if code:
            countryobj.code = code

        if new_slug:
            countryobj.slug = new_slug

        if flag:
            countryobj.flag = flag

        if state_available is not None:
            countryobj.is_state_available = state_available == '1'

        countryobj.save()
        return JsonResponse({'message': 'Country updated successfully'})
    
    def delete(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

        slug = data.get('slug')
        if not slug:
            return JsonResponse({'message': 'Slug is required'}, status=400)

        try:
            countryobj = Country.objects.get(slug=slug)
        except Country.DoesNotExist:
            return JsonResponse({'message': 'Country not found'}, status=404)
        
        countryobj.delete()
        return JsonResponse({'message': 'Country deleted successfully'})

#Create API for State -> get, post, put, delete
class StateApiView(View):
    def get(self, request, slug=None):
        if slug is None:
            return JsonResponse({'error': 'Country slug is required'}, status=400)
        
        countryobj = Country.objects.get(slug=slug)

        if not countryobj:
            return JsonResponse({'error': 'Country not found'}, status=404)
        stateobj = State.objects.filter(country=countryobj)

# Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(stateobj, 5)  # Show 5 states per page

        stateobj = paginator.get_page(page)

        statelist = []
        for item in stateobj:
            statedata = {}
            statedata['name'] = item.name
            statedata['slug'] = item.slug
            statedata['country'] = item.country.name
            statelist.append(statedata)
            return JsonResponse(statelist, safe=False)
        
        response_data = {
            'country': {
                'name': countryobj.name,
                'slug': countryobj.slug
            },
            'states': statelist,
            'page': stateobj.number,
            'num_pages': paginator.num_pages,
            'has_next': stateobj.has_next(),
            'has_previous': stateobj.has_previous()
        }

        return JsonResponse(response_data)
        
    def post(self,request,slug=None):
        state_name = request.POST.get('state_name')
        state_slug = request.POST.get('state_slug')
        language = request.POST.get('language')
        population = request.POST.get('population')

        if State.objects.filter(slug=state_slug).exists():
            context = {'message': 'State slug is already exist'}
            return JsonResponse(context)
        
        if Country.objects.filter(name=state_name).exists():
            context = {'message': 'State name is already exist'}
            return JsonResponse(context)
        
        countryobj = Country.objects.get(slug = slug)

        State.objects.create(
            country=countryobj, 
            name=state_name,
            slug=state_slug,
            language=language,
            population=population,
        )
        context = {'message': 'State added successfully'}
        return JsonResponse(context)
    
    def put(self, request, slug=None):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

        slug = data.get('slug')
        if not slug:
            return JsonResponse({'message': 'Slug is required'}, status=400)

        # Fetch state object using provided slug
        try:
            stateobj = State.objects.get(slug=slug)
        except State.DoesNotExist:
            return JsonResponse({'message': 'State not found'}, status=404)
        
        state_name = data.get('state_name')
        new_state_slug = data.get('new_state_slug')
        language = data.get('language')
        population = data.get('population')

        if state_name:
            stateobj.name=state_name
        if new_state_slug:
            stateobj.slug=new_state_slug
        if language:
            stateobj.language=language
        if population:
            stateobj.population=population

        stateobj.save()
        context = {'message': 'State updated successfully'}
        return JsonResponse(context)

    def delete(self, request, slug=None):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

        slug = data.get('slug')
        if not slug:
            return JsonResponse({'message': 'Slug is required'}, status=400)

        # Fetch state object using provided slug
        try:
            stateobj = State.objects.get(slug=slug)
        except State.DoesNotExist:
            return JsonResponse({'message': 'State not found'}, status=404)
        
        stateobj.delete()
        context = {'message': 'State deleted successfully'}
        return JsonResponse(context)
    
# Create API for City -> get, post, put, delete
class CityApiView(View):
    def get(self, request, slug=None):
        if slug is None:
            return JsonResponse({'error': 'Country slug is required'}, status=400)
        
        stateobj = State.objects.get(slug=slug)

        if not stateobj:
            return JsonResponse({'error': 'State not found'}, status=404)
        
        cityobj = City.objects.filter(state=stateobj)

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(cityobj, 5)  # Show 5 states per page

        cityobj = paginator.get_page(page)

        citylist = []
        for item in cityobj:
            citydata = {}
            citydata['name'] = item.name
            citydata['slug'] = item.slug
            citydata['country'] = item.country.name
            citydata['state'] = item.state.country.name
            citylist.append(citydata)
            return JsonResponse(citylist, safe=False)
        
    def post(self, request, slug=None):
        city_name = request.POST.get('city_name')
        city_slug = request.POST.get('city_slug')

        if City.objects.filter(name=city_name).exists():
            context = {'message': 'City already exist for this state'}
            return JsonResponse(context)
        
        try:
            stateobj = State.objects.get(slug=slug)
        except State.DoesNotExist:
            return JsonResponse({'message': 'State not found'}, status=404)
        
        City.objects.create(
            country=stateobj.country,
            state=stateobj,
            name=city_name,
            slug=city_slug,
        )
        context = {'message': 'City added successfully'}
        return JsonResponse(context)

    def put(self, request, slug=None):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

        slug = data.get('slug')
        if not slug:
            return JsonResponse({'message': 'Slug is required'}, status=400)

        # Fetch state object using provided slug
        try:
            cityobj = City.objects.get(slug=slug)
        except State.DoesNotExist:
            return JsonResponse({'message': 'City not found'}, status=404)
        
        city_name = data.get('city_name')
        new_city_slug = data.get('new_city_slug')

        cityobj = City.objects.get(slug=slug)

        if city_name:
            cityobj.name = city_name
        if new_city_slug:
            cityobj.slug = new_city_slug

        cityobj.save()
        context = {'message': 'City updated successfully'}
        return JsonResponse(context)
    
    def delete(self, request, slug=None):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

        slug = data.get('slug')
        if not slug:
            return JsonResponse({'message': 'Slug is required'}, status=400)

        # Fetch state object using provided slug
        try:
            cityobj = City.objects.get(slug=slug)
        except State.DoesNotExist:
            return JsonResponse({'message': 'City not found'}, status=404)
        
        cityobj.delete()
        context = {'message': 'City deleted successfully'}
        return JsonResponse(context)
    