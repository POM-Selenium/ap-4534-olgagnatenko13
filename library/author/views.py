from django.shortcuts import render, redirect
from author.models import Author
from .forms import AuthorForm


def authors_list(request):
    if request.user.role != 1:
        return redirect('/')
    authors = Author.get_all()
    return render(request, 'authors/list.html', {'authors': authors})


def author_create(request):
    if request.user.role != 1:
        return redirect('/')

    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            Author.create(
                form.cleaned_data['name'],
                form.cleaned_data['surname'],
                form.cleaned_data['patronymic'],
            )
            return redirect('/authors/')
    else:
        form = AuthorForm()

    return render(request, 'authors/create.html', {'form': form})


def author_edit(request, author_id):
    if request.user.role != 1:
        return redirect('/')

    author = Author.get_by_id(author_id)
    if not author:
        return redirect('/authors/')

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author.name = form.cleaned_data['name']
            author.surname = form.cleaned_data['surname']
            author.patronymic = form.cleaned_data['patronymic']
            author.save()
            return redirect('/authors/')
    else:
        form = AuthorForm(initial={
            'name': author.name,
            'surname': author.surname,
            'patronymic': author.patronymic,
        })

    return render(request, 'authors/edit.html', {'form': form, 'author': author})


def author_delete(request, author_id):
    if request.user.role != 1:
        return redirect('/')
    author = Author.get_by_id(author_id)
    if author and not author.books.exists():
        author.delete()
    return redirect('/authors/')