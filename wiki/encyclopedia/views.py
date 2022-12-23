from django.shortcuts import render
#list_entries, save_entry, get_entry
from markdown2 import Markdown
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from random import choice
from django.core.exceptions import ValidationError
markdown = Markdown()

class SearchForm(forms.Form):
    """ Django Form for searches of all markdown file entries """
    search = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}))

class NewEntryForm(forms.Form):
    """ Django Form for user to enter a new markdown entry """
    title = forms.CharField(label="Title", 
        widget=forms.TextInput(attrs={'placeholder':'Title for page reference', 
            'style': 'width: 300px;', 'class': 'form-control'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
            'placeholder':'Please include "#" before the page header, e.g. # Javascript. "*" can be used to add a bullet point', 
            'style': 'width: 800px;', 'class': 'form-control'}))

def new_entry(request):
    """ Renders new_entry.html page with form for new entry (title and content). Directs user to new entry page on form submission."""
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            all_entries = util.list_entries()
            for entry in all_entries:
                if util.get_entry(title):
                    exists = form.cleaned_data['title']              
                    new_entry = NewEntryForm()
                    context = {"entry_form": new_entry, "form": SearchForm(), "exists": exists, "dupe": exists}
                    return render(request, "encyclopedia/error.html", context)
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            named_redirect = reverse('entry', args=[title])
            return HttpResponseRedirect(named_redirect)
        
    else:
        new_entry = NewEntryForm()
        context = {"entry_form": new_entry, "form": SearchForm()}
        return render(request, "encyclopedia/new_entry.html", context)

def error(request):
    """ Informs user if new entry title is already in use."""
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            exists = form.cleaned_data['title']              
            new_entry = NewEntryForm()
            context = {"entry_form": new_entry, "form": SearchForm(), "exists": exists}
            return render(request, "encyclopedia/error.html", context)
        
    return render(request, "encyclopedia/error.html")

def index(request):
    """ Renders Index page with all markdown entries """
    if request.method == "POST":
        form = SearchForm(request.POST)
        all_entries = util.list_entries()
        
        if form.is_valid():
            search_term = form.cleaned_data["search"]
            for entry in all_entries:

                    if search_term == entry:
                        context = {"search": search_term}
                        named_redirect = reverse('entry', args=[search_term])
                        return HttpResponseRedirect(named_redirect, context)
                    
                    if search_term in entry:
                        context = {"entry": entry, "all": all_entries, "term": search_term, "form": SearchForm()}
                        return render(request, "encyclopedia/suggestion.html", context)
            
                    if search_term.lower() == entry.lower(): 
                        named_redirect = reverse('entry', args=[entry])
                        return HttpResponseRedirect(named_redirect)

                    else:
                        continue

            if search_term not in all_entries:        
                        context = { "term": search_term, "form": SearchForm() }
                        return render(request, "encyclopedia/no_valid_entry.html", context)
                
    else:
        context = {"entries": util.list_entries(), "form": SearchForm()}
        return render(request, "encyclopedia/index.html", context)

def search(request):
    """ Directs user to desired page through SearchForm """

    if request.method == "POST":
        form = SearchForm(request.POST)
        all_entries = util.list_entries()
        
        if form.is_valid():
            search_term = form.cleaned_data["search"]
            for entry in all_entries:

                    if search_term == entry:
                        context = {"search": search_term}
                        named_redirect = reverse('entry', args=[search_term])
                        return HttpResponseRedirect(named_redirect, context)
                    
                    if search_term in entry:
                        context = {"entry": entry, "all": all_entries, "term": search_term, "form": SearchForm()}
                        return render(request, "encyclopedia/suggestion.html", context)
            
                    if search_term.lower() == entry.lower(): 
                        #named_redirect = reverse()
                        #return HttpResponseRedirect('suggestion')
                        named_redirect = reverse('entry', args=[entry])
                        return HttpResponseRedirect(named_redirect)
                        ##context = {"entry": entry}
                        ##return render(request, "encyclopedia/suggestion.html", context)"""

                    else:
                        continue

            if search_term not in all_entries:        
                        context = { "term": search_term, "form": SearchForm() }
                        return render(request, "encyclopedia/no_valid_entry.html", context)
            else:
                context = {"entries": util.list_entries(), "form": SearchForm()}
                return render(request, "encyclopedia/index.html", context)
                
    else:
        context = {"entries": util.list_entries(), "form": SearchForm()}
        return render(request, "encyclopedia/index.html", context)

def entry(request, entry):
    """ Allows user to create a new entry """

    if request.method == "POST":
        if SearchForm(request.POST):
            form = SearchForm(request.POST)
            search_term = form.cleaned_data["search"]

    if util.get_entry(entry):
        title = entry 
        full_entry = util.get_entry(entry)
        converted_entry = markdown.convert(full_entry)
        context = {"converted_entry": converted_entry, "title": title, "form": SearchForm()}
        return render(request,"encyclopedia/entry.html", context)
 
    else:
        context = {"entry": entry, "form":SearchForm()}
        return render(request, "encyclopedia/no_valid_entry.html", context)

def edit(request):
    """ Allows user to edit an entry"""
    entry_title = request.POST['edit_entry']
    entry_content = util.get_entry(entry_title)
    edit_form = NewEntryForm({'title': entry_title, 'content': entry_content})
    context = {"edit_form": edit_form, "title": entry_title, "content": entry_content, "form": SearchForm()}
    return render(request, "encyclopedia/edit.html", context)

def save(request):
    """ Allows user to save new entry. Directs to new entry page """
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            converted_entry = markdown.convert(content)
            context = {"title": title, "converted_entry": converted_entry, "form": SearchForm()}
            return render(request, 'encyclopedia/entry.html', context)

def thanks(request):
    """ Redundant """
    return render(request, "encyclopedia/thanks.html")

def rando(request):
    """ Takes user to a random entry """
    entries_list = util.list_entries()
    selection = choice(entries_list)
    random_content = util.get_entry(selection)
    converted_entry = markdown.convert(random_content)
    context = {"converted_entry": converted_entry, "title": selection, "form": SearchForm()}
    return render(request,"encyclopedia/entry.html", context)
