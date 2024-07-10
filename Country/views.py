from django.shortcuts import render, redirect
from django.views import View
from .models import Country, State, City
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create Country.
class CountryView(View):
    def get(self, request, slug=None):
        if slug:
            countryobj = Country.objects.get(slug = slug)
            if countryobj.is_active:
                countryobj.is_active = False    
                countryobj.save()
            else:
                countryobj.is_active = True    
                countryobj.save()
            return redirect('/')
        else:
            countryobj = Country.objects.all()

            # Pagination
            page = request.GET.get('page', 1)
            paginator = Paginator(countryobj, 5)  # Show 5 country per page

            try:
                countryobj = paginator.page(page)
            except PageNotAnInteger:
                countryobj = paginator.page(1)
            except EmptyPage:
                countryobj = paginator.page(paginator.num_pages)

            context = {'countryobj': countryobj}
            return render(request, 'html/country.html', context)
    
    def post(self, request, slug=None):
        if slug:
            countryobj = Country.objects.get(slug=slug)
            countryobj.delete()
            return redirect('/')
        else:
            country_name = request.POST.get('country_name')
            slug = request.POST.get('slug')
            code = request.POST.get('code')
            flag = request.FILES.get('flag')
            state_available = request.POST.get('state_available') == '1' #convert to boolean

        if not state_available:
            state_available=False

        if Country.objects.filter(code=code).exists():
            messages.error (request, f"{code} is already exist!")
            return redirect('/')
        
        if Country.objects.filter(slug=slug).exists():
            messages.error (request, f"{slug} is already exist!")
            return redirect('/')
        
        if Country.objects.filter(name=country_name).exists():
            messages.error(request, f"The country '{country_name}' already exists!")
            return redirect('/')
        
        Country.objects.create(
            name=country_name, 
            slug=slug, 
            code=code, 
            flag=flag, 
            is_state_available=state_available)
        messages.success (request, f"Country created successfully!")
        return redirect('/')

#Create Update Country 
class UpdateCountry(View):
    def get(self, request, slug=None):
        countryobj = Country.objects.get(slug = slug)
        context = {'countryobj': countryobj}
        return render(request, 'html/countupdate.html', context)
    
    def post(self, request, slug=None):
        country_name = request.POST.get('country_name')
        newslug = request.POST.get('slug')
        code = request.POST.get('code')
        flag = request.FILES.get('flag')
        state_available = request.POST.get('state_available') == '1'

        countryobj = Country.objects.get(slug = slug)   

        if country_name:
            countryobj.name = country_name

        if newslug:
            countryobj.slug = newslug

        if code:
            countryobj.code = code

        if flag:
            countryobj.flag = flag

        if not state_available:
            state_available=False
            countryobj.is_state_available = state_available
        else:
            countryobj.is_state_available = True

        countryobj.save()
        messages.success(request, "Country updated successfully!")
        return redirect('/')
    
#create state
class StateView(View):
    def get(self, request, slug=None):

        countryobj = Country.objects.get(slug=slug)
        stateobj =  State.objects.filter(country = countryobj)

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(stateobj, 5)  # Show 5 state per page

        try:
            stateobj = paginator.page(page)
        except PageNotAnInteger:
            stateobj = paginator.page(1)
        except EmptyPage:
            stateobj = paginator.page(paginator.num_pages)

        context = {'countryobj': countryobj, 'stateobj':stateobj }
        return render(request, 'html/state.html', context)
    
    def post(self, request, slug=None):
        state_name = request.POST.get('state_name')
        state_slug = request.POST.get('state_slug')
        language = request.POST.get('language')
        population = request.POST.get('population')

        if State.objects.filter(slug=state_slug).exists():
            messages.error (request, f"{state_slug} is already exist!")
            return redirect(f'/state/{slug}')
        
        if State.objects.filter(name=state_name).exists():
            messages.error(request, f"The State '{state_name}' already exists!")
            return redirect(f'/state/{slug}')
        
        countryobj = Country.objects.get(slug = slug)

        State.objects.create(
            country=countryobj, 
            name=state_name,
            slug=state_slug,
            language=language,
            population=population,
        )
        messages.success (request, "State added successfully!")
        return redirect(f'/state/{slug}')

#create update state 
class UpdateState(View):
    def get(self, request, slug=None):
        stateobj = State.objects.get(slug = slug) 
        countryobj = stateobj.country
        context = {'countryobj': countryobj, 'stateobj':stateobj }
        return render(request, 'html/stateupdate.html', context)
    
    def post(self, request, slug=None):
        state_name = request.POST.get('state_name')
        state_slug = request.POST.get('state_slug')
        language = request.POST.get('language')
        population = request.POST.get('population')

        stateobj = State.objects.get(slug=slug)

        if state_name:
            stateobj.name=state_name
        if state_slug:
            stateobj.slug=state_slug
        if language:
            stateobj.language=language
        if population:
            stateobj.population=population

        stateobj.save()
        messages.success(request, "State updated successfully!")
        return redirect(f'/state/{stateobj.country.slug}')

#create state delete
class DeleteState(View):
    def get(self, request, slug=None):
        stateobj = State.objects.get(slug=slug)
        stateobj.delete()
        messages.success(request, "State deleted successfully!")
        return redirect(f'/state/{stateobj.country.slug}')

# Toggle state active/inactive status
class ToggleStateActive(View):
    def get(self, request, slug=None):
        stateobj = State.objects.get(slug=slug)
        stateobj.is_active = not stateobj.is_active
        stateobj.save()
        messages.success(request, f"State {'activated' if stateobj.is_active else 'deactivated'} successfully!")
        return redirect(f'/state/{stateobj.country.slug}')
    
class CityView(View):
    def get(self, request, slug=None, countryslug=None, stateslug=None):
        if slug:
            countryobj = Country.objects.get(slug=slug)
            cityobj = City.objects.filter(country=countryobj)
            paginator = Paginator(cityobj, 5)  # Show 5 cities per page
            page_number = request.GET.get('page')
            try:
                cityobj = paginator.page(page_number)
            except PageNotAnInteger:
                cityobj = paginator.page(1)
            except EmptyPage:
                cityobj = paginator.page(paginator.num_pages)
            context = {'countryobj': countryobj, 'cityobj': cityobj, 'from_country': True}
            return render(request, 'html/city.html', context)
        else:
            countryobj = Country.objects.get(slug=countryslug)
            stateobj = State.objects.get(slug=stateslug)
            cityobj = City.objects.filter(state=stateobj)
            paginator = Paginator(cityobj, 5)  # Show 5 cities per page
            page_number = request.GET.get('page')
            try:
                cityobj = paginator.page(page_number)
            except PageNotAnInteger:
                cityobj = paginator.page(1)
            except EmptyPage:
                cityobj = paginator.page(paginator.num_pages)
            context = {'countryobj': countryobj, 'stateobj': stateobj, 'cityobj': cityobj, 'from_state': True}
            return render(request, 'html/city.html', context)

    def post(self, request, slug=None, countryslug=None, stateslug=None):
        if slug:
            city_name = request.POST.get('city_name')
            city_slug = request.POST.get('city_slug')
            countryobj = Country.objects.get(slug=slug)

            if City.objects.filter(name=city_name).exists():
                messages.error(request, f"The city '{city_name}' already exists for this country!")
                return redirect(f'/city/{slug}')

            City.objects.create(
                country=countryobj,
                name=city_name,
                slug=city_slug,
            )
            messages.success(request, "City added successfully!")
            return redirect(f'/city/{slug}')
        else:
            city_name = request.POST.get('city_name')
            city_slug = request.POST.get('city_slug')
            countryobj = Country.objects.get(slug=countryslug)
            stateobj = State.objects.get(slug=stateslug)

            if City.objects.filter(name=city_name).exists():
                messages.error(request, f"The city '{city_name}' already exists for this state!")
                return redirect(f'/city/{countryslug}/{stateslug}')

            City.objects.create(
                country=countryobj,
                state=stateobj,
                name=city_name,
                slug=city_slug,
            )
            messages.success(request, "City added successfully!")
            return redirect(f'/city/{countryslug}/{stateslug}')
            
class UpdateCity(View):
    def get(self, request, slug=None):
        cityobj = City.objects.get(slug=slug)
        stateobj = cityobj.state
        countryobj = cityobj.country
        context = {'countryobj': countryobj, 'stateobj': stateobj, 'cityobj': cityobj}
        return render(request, 'html/cityupdate.html', context)

    def post(self, request, slug=None):
        city_name = request.POST.get('city_name')
        city_slug = request.POST.get('city_slug')

        cityobj = City.objects.get(slug=slug)

        if city_name:
            cityobj.name = city_name
        if city_slug:
            cityobj.slug = city_slug

        cityobj.save()
        messages.success(request, "City updated successfully!")
        if cityobj.state:
            return redirect(f'/city/{cityobj.country.slug}/{cityobj.state.slug}')
        else:
            return redirect(f'/city/{cityobj.country.slug}')

# # Delete City
class DeleteCity(View):
    def get(self, request, slug=None):
        cityobj = City.objects.get(slug=slug)
        cityobj.delete()
        messages.success(request, "City deleted successfully!")
        return redirect(f'/state/{cityobj.country.slug}')
    
# Toggle City active/inactive status
class ToggleCityActive(View):
    def get(self, request, slug=None):
        cityobj = City.objects.get(slug=slug)
        cityobj.is_active = not cityobj.is_active
        cityobj.save()
        messages.success(request, f"City {'activated' if cityobj.is_active else 'deactivated'} successfully!")
        if cityobj.state:
            return redirect(f'/city/{cityobj.country.slug}/{cityobj.state.slug}')
        else:
            return redirect(f'/city/{cityobj.country.slug}')

    