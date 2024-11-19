# from django.shortcuts import redirect, render
# from .forms import AlumniForm
# from .models import Alumni

# # Create your views here.
# def alumniFormView(request):
#     form = AlumniForm()
#     if request.method == 'POST':
#         form = AlumniForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('show_url')
#     template_name = 'myapp/Alumni.html'
#     context = {'form': form}
#     return render(request, template_name, context)

# def showView(request):
#     obj = Alumni.objects.all()
#     template_name = 'myapp/show.html'
#     context = {'obj': obj}
#     return render(request, template_name, context)

# def updateView(request, f_id):
#     obj = Alumni.objects.get(id=f_id)
#     form = AlumniForm(instance=obj)
#     if request.method == 'POST':
#         form = AlumniForm(request.POST, instance=obj)
#         if form.is_valid():
#             form.save()
#             return redirect('show_url')
#     template_name = 'myapp/alumni.html'
#     context = {'form': form}
#     return render(request, template_name, context)

# def deleteView(request, f_id):
#     obj = Alumni.objects.get(id=f_id)
#     if request.method == 'POST':
#         obj.delete()
#         return redirect('show_url')
#     template_name = 'myapp/confirmation.html'
#     context = {'obj': obj}
#     return render(request, template_name, context)

# alumni/views.py
from django.db.models import Q
import csv
from django.http import HttpResponse
from .models import Alumni
# alumni/views.py
import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Alumni
from .forms import AlumniForm
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .models import Alumni
import pandas as pd
import time

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Alumni
from .forms import AlumniForm
from django.contrib import messages

# Dashboard - show all alumni records
def dashboard(request):
    alumni = Alumni.objects.all()
    return render(request, 'myapp/dashboard.html', {'alumni': alumni})

# Show details for a specific alumni
def alumni_detail(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    return render(request, 'myapp/alumni_detail.html', {'alumni': alumni})

# Update Alumni details
def alumni_update(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    if request.method == 'POST':
        form = AlumniForm(request.POST, instance=alumni)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated {alumni.full_name}')
            return redirect('dashboard')
    else:
        form = AlumniForm(instance=alumni)
    return render(request, 'myapp/alumni_form.html', {'form': form, 'alumni': alumni})

# Delete an alumni record
def alumni_delete(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    if request.method == 'POST':
        alumni.delete()
        messages.success(request, f'{alumni.full_name} has been deleted.')
        return redirect('dashboard')
    return render(request, 'myapp/alumni_confirm_delete.html', {'alumni': alumni})

# List Alumni
def alumni_list(request):
    alumni = Alumni.objects.all()
    
    # Search functionality
    query = request.GET.get('search')
    if query:
        alumni = alumni.filter(
            Q(full_name__icontains=query) | 
            Q(university_affiliation__icontains=query)
        )

    # Sorting functionality
    sort_by = request.GET.get('sort', 'full_name')
    alumni = alumni.order_by(sort_by)

    return render(request, 'myapp/alumni_list.html', {'alumni': alumni})

def alumni_create(request):
    if request.method == 'POST':
        form = AlumniForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alumni_list')
        else:
            print("Form is not valid:")
            print(form.errors)  # Log validation errors
    else:
        form = AlumniForm()
    return render(request, 'myapp/alumni_form.html', {'form': form})

# Update Alumni details
def alumni_update(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    if request.method == 'POST':
        form = AlumniForm(request.POST, instance=alumni)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated {alumni.full_name}')
            return redirect('dashboard')
    else:
        form = AlumniForm(instance=alumni)
    return render(request, 'myapp/alumni_form.html', {'form': form, 'alumni': alumni})

# Delete an alumni record
def alumni_delete(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    if request.method == 'POST':
        alumni.delete()
        messages.success(request, f'{alumni.full_name} has been deleted.')
        return redirect('dashboard')
    return render(request, 'myapp/alumni_confirm_delete.html', {'alumni': alumni})

# def alumni_list(request):
#     alumni = Alumni.objects.all()
#     query = request.GET.get('search')
#     if query:
#         alumni = alumni.filter(
#             Q(full_name__icontains=query) | 
#             Q(university_affiliation__icontains=query)
#         )
#     sort_by = request.GET.get('sort', 'full_name')
#     alumni = alumni.order_by(sort_by)
#     return render(request, 'myapp/alumni_list.html', {'alumni': alumni})
def alumni_list(request):
    alumni = Alumni.objects.all()

    # Optional: Log the queryset for debugging
    # print("Alumni records:", alumni)

    query = request.GET.get('search')
    if query:
        alumni = alumni.filter(
            Q(full_name__icontains=query) | 
            Q(university_affiliation__icontains=query)
        )

    sort_by = request.GET.get('sort', 'full_name')
    alumni = alumni.order_by(sort_by)

    return render(request, 'myapp/alumni_list.html', {'alumni': alumni})

def export_alumni_csv(request):
    alumni = Alumni.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumni.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Affiliation', 'Date of Death'])
    
    for a in alumni:
        writer.writerow([a.full_name, a.university_affiliation, a.date_of_death])
    
    return response

# Base URL for the obituaries list
base_url = "https://windsorstar.remembering.ca"

# List to store scraped details
all_obituaries = []

# Function to get the list of obituaries and extract the detail page links
def get_obituaries_list(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to fetch list page: {page_url}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    obituary_links = []

    # Find each obituary link on the list page
    for entry in soup.find_all("a", href=True):
        if entry["href"].startswith("/obituary/"):
            obituary_links.append(base_url + entry["href"])

    return obituary_links

# Function to scrape details from each obituary page
def scrape_obituary_details(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch detail page: {url}")
        return None
    
    soup = BeautifulSoup(response.content, "html.parser")
    data = {"URL": url}

    # First Name and Last Name
    name_tag = soup.find("h1", class_="obit-name")
    if name_tag:
        full_name = name_tag.get_text(strip=True).replace("\n", " ").strip()
        parts = full_name.split()
        data["First Name"] = " ".join(parts[:-1])
        data["Last Name"] = parts[-1] if len(parts) > 1 else ""

    # Date of Birth and Date of Death
    dates_tag = soup.find("h2", class_="obit-dates")
    if dates_tag:
        dates = dates_tag.get_text(strip=True).split("-")
        data["Date of Birth"] = dates[0].strip() if len(dates) > 0 else ""
        data["Date of Death"] = dates[1].strip() if len(dates) > 1 else ""

    # Description
    description_tag = soup.find("p", class_="set-font")
    if description_tag:
        data["Description"] = " ".join(description_tag.stripped_strings)

    return data

# Django view to sync data from the obituary website
def sync_data(request):
    if request.method == 'POST':
        try:
            # URL of the first page (Modify for other pages if necessary)
            list_page_url = f"{base_url}/obituaries/obituaries/search?limit=125&p=1"

            # Get list of obituaries
            obituary_links = get_obituaries_list(list_page_url)

            # Loop through each obituary link and scrape details
            for index, url in enumerate(obituary_links, start=1):
                print(f"Scraping obituary {index}/{len(obituary_links)}: {url}")
                details = scrape_obituary_details(url)
                if details:
                    # Saving the data to the Alumni model
                    alumni, created = Alumni.objects.update_or_create(
                        full_name=details["First Name"] + " " + details["Last Name"],
                        university_affiliation="University of Windsor",  # Adjust if you have a way to grab this info
                        defaults={
                            'date_of_death': details.get("Date of Death"),
                            'obituary_url': details["URL"],
                            'notable_info': details.get("Description"),
                        }
                    )
                    if created:
                        print(f"Added new alumni: {details['First Name']} {details['Last Name']}")
                    else:
                        print(f"Updated alumni: {details['First Name']} {details['Last Name']}")
                time.sleep(1)  # Be polite and avoid overloading the server

            messages.success(request, "Data synchronization completed successfully!")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Network error: {e}")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        return redirect('sync_data')  # Redirect back to the sync page to show message

    return render(request, 'myapp/sync_data.html')  # Render the sync data page