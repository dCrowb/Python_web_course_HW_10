from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views import View

from .forms import AuthorForm, QuoteForm
from .models import Author, Tag, Quote

def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10  
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(
        page
    )
    return render(request, "quotesapp/index.html", context={"quotes": quotes_on_page})


def about(request, quote_id):
    author_id = Quote.objects.get(id=quote_id).author_id
    description = Author.objects.get(id=author_id)
    return render(request, "quotesapp/description.html", context={"authors": description})


def authors_by_tags(request, tag_name):
    tags = Tag.objects.get(name=tag_name)
    quotes = tags.quote_set.all()
    return render(request, "quotesapp/tags.html", context={"quotes": quotes})


class AuthorView(View):
    template_name = 'quotesapp/add_author.html'
    form_class = AuthorForm
    model = Author

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()  # Запис у БД
            return redirect(to='quotesapp:root')
        return render(request, self.template_name, {"form": form})


class QuoteView(View):
    template_name = 'quotesapp/add_quote.html'
    form_class = QuoteForm
    model = Quote

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:root')

        return render(request, self.template_name, {"form": form})