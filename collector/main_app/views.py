from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Bird , Toy
from django.views.generic.edit import UpdateView, DeleteView , CreateView
from django.views.generic import ListView , DetailView
from .forms import FeedingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


class BirdCreate(CreateView):
    model = Bird
    # fields = '__all__'  If a stand alone model use this line otherwise restrict user
    fields = ['name', 'breed', 'description', 'age', 'image']
    # success_url = '/cats/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BirdUpdate(UpdateView):
    model = Bird
    fields = ['breed', 'description', 'age']

class BirdDelete(DeleteView):
    model = Bird
    success_url = '/birds/'

# toys CRUD
class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name' , 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    # return HttpResponse("<h1>About the cat collector</h1>")
    return render(request, 'about.html')

@login_required
def birds_index(request):
    # Select * from main_app_cat;
    # cats = CAT.objects.all()
    birds = Bird.objects.filter(user = request.user)
    return render(request, 'birds/index.html', {'birds': birds})

@login_required
def bird_detail(request, bird_id):
    bird = Bird.objects.get(id=bird_id)
    feeding_form = FeedingForm()

    # Exclude those toys ids which exists in cat_toys join table with the current cat id 
    # remaining toys ids will be returend to toys_cat_doent_have
    toys_cat_doent_have = Toy.objects.exclude(id__in = bird.toys.all().values_list('id'))
    return render(request, 'birds/detail.html' , {'bird': bird, 'feeding_form': feeding_form, 'toys': toys_cat_doent_have})

@login_required
def add_feeding(request , bird_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.bird_id = bird_id
        new_feeding.save()
        return redirect('detail', bird_id=bird_id)
    
@login_required
def assoc_toy(request , bird_id , toy_id):
    Bird.objects.get(id=bird_id).toys.add(toy_id)
    return redirect('detail', bird_id = cat_id)

@login_required
def unassoc_toy(request , bird_id , toy_id):
    CAT.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', bird_id = bird_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('index')
        else:
            error_message = 'Invalid signup - please try again later.'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

