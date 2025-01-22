from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import guides
from django.core.paginator import Paginator
import csv


def CSV(request):
    # data_frame = pandas.read_csv('app1/Static/Data.csv')
     
    with open('guide/static/Data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                m=guides.objects.get(mname=row['mname'])
                print(m)
            except:
                print("not same")
                p = guides(mname=row['mname'], category=row['category'],unit=row['unit'],unit_price = row['unit_price'],package_unit = row['package_unit'],package_price = row['package_price'],drug= row['drug'],per_unit = row['per_unit'],indication = row['indication'],contraindication = row['contraindication'],caution = row['caution'],side_effect = row['side_effect'])
                p.save()
    
    guide= guides.objects.all()
    paginator = Paginator(guide, 5) # Show 5 medicines per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Medicine.html', {'key':guide,'page_obj': page_obj})

def View(request, pk):
    guide= get_object_or_404(guides,id=pk)    
    return render(request,'view.html',{'key':guide})
