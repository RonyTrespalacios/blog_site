from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, ContactForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
import markdown
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.models import User

def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    
    # Convierte el contenido de Markdown a HTML con las extensiones necesarias
    content_in_markdown = markdown.markdown(
        post.content, 
        extensions=['fenced_code', 'codehilite']
    )
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'content': mark_safe(content_in_markdown)
    })

def about(request):
    return render(request, 'blog/about.html', {'title': 'Acerca de'})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Asume que el modelo Post tiene un campo author
            post.save()
            return redirect('blog:home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Crear Publicación'})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Aquí podrías manejar los datos, como guardarlos en una base de datos
            return render(request, 'blog/contact_success.html')
    else:
        form = ContactForm()
    
    return render(request, 'blog/contact.html', {'form': form, 'title': 'Contáctame'})

@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    
    if post.author != request.user and not request.user.is_staff:
        raise PermissionDenied  # Deniega acceso si no es el autor o admin
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.date_posted = timezone.now()  # Actualiza la fecha de publicación
            post.save()
            return redirect('blog:post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Editar Publicación'})

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    
    if post.author != request.user and not request.user.is_staff:
        raise PermissionDenied  # Deniega acceso si no es el autor o admin
    
    if request.method == 'POST':
        post.delete()
        return redirect('blog:home')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post, 'title': 'Eliminar Publicación'})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:login')  # Cambia esto si quieres redirigir a otra parte después de registrarse
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def home(request):
    # Obtener los parámetros de filtrado y ordenación de la URL
    author = request.GET.get('author')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    order_by = request.GET.get('order_by')

    # Filtrar los posts según los parámetros recibidos
    posts = Post.objects.all()

    if author:
        posts = posts.filter(author__username=author)
    
    if start_date and end_date:
        posts = posts.filter(date_posted__range=[start_date, end_date])
    
    # Ordenar según el parámetro order_by
    if order_by:
        posts = posts.order_by(order_by)
    else:
        posts = posts.order_by('-date_posted')  # Orden por defecto: fecha descendente

    users = User.objects.all()

    return render(request, 'blog/home.html', {'posts': posts, 'users': users})
