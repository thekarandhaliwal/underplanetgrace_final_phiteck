from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
from django.conf import settings
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PlanetData
from .serializers import PlanetDataSerializer
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import json
# from rest_framework import routers, serializers, viewsets
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.conf import settings

import threading
from pdf2image import convert_from_path
import os, re

def convert(request):
    return render(request, 'newunder.html')

@method_decorator(csrf_exempt, name='dispatch')
class UnderPlanetGrace(APIView):
    @csrf_exempt
    def get(self, request):
    
        order_no = request.GET.get('order_no')
        # order = PlanetData.objects.all()
        planetdata = PlanetData.objects.get(order=order_no)
        serializer = PlanetDataSerializer(planetdata, many=True, context={"request": request})
        response_data = serializer.data
        print(response_data)
        return Response(response_data)
    

    @csrf_exempt
    def post(self, request):

        # planetdata = json.loads(request.data)
        planetdata = request.data
        boolean_fields = ['properties[Pluto]', 'properties[Orbit Line]','properties[Day Chart]', 'properties[Zodiac Wheel]', 'properties[Moon]']
        for field in boolean_fields:
            if field in planetdata:
                if planetdata[field].lower() == 'Yes':
                    planetdata[field] = True
                else:
                    planetdata[field] = False


        # print(planetdata)
        db = PlanetData.objects.create(
            order_no=planetdata['order_no'],
            # id = planetdata['id'],
            design=planetdata['properties[Design]'],
            poster=planetdata['properties[Poster]'],
            pluto=planetdata['properties[Pluto]'],
            orbitline=planetdata['properties[Orbit Line]'],
            daychart=planetdata['properties[Day Chart]'],
            zodiacwheel=planetdata['properties[Zodiac Wheel]'],
            moon=planetdata['properties[Moon]'],
            datetime=planetdata['properties[Date]'],
            locationselect=planetdata['properties[Location Select]'],
            titletext=planetdata['properties[Title Text]'],
            defaultfnote=planetdata['properties[Defaultf Note]'],
            specialmoment=planetdata['properties[Special Moment]'],
            size = planetdata['Size'],
            posteronly=planetdata['properties[Poster Only]'],
            woodenframe=planetdata['properties[Wooden Frame]'],
            matelframe=planetdata['properties[Metal Frame]'],
            hanger=planetdata['properties[Hanger]'],
            solarsystem_content=planetdata['solarsystem_content'],
            selected_poster=planetdata['selected_poster']
        )

        

        serializer = PlanetDataSerializer(db, many=False, context={"request": request})
        entry_id = db.id
        entry_id_str = str(entry_id)
        planetdata = get_object_or_404(PlanetData, id=entry_id)

        db.download_url="http://127.0.0.1:8000/media/pdf/"+entry_id_str+".jpg"
        db.save()


        t = threading.Thread(target=background_process, args=(planetdata, request), kwargs={})
        t.setDaemon(True)
        t.start()
        # background_process(planetdata, request)
        

        return Response(serializer.data)

def background_process(planetdata, request):
    if planetdata.size == "Starter":
        pageWidth = '304.8mm'
        pageHeight = '406.4mm'
        template = 'starter.html'
        zoom = 3.10

    elif planetdata.size == "Standard":
        pageWidth = '457.2mm'
        pageHeight = '609.6mm'
        template = 'standard.html'
        zoom = 4.75

    elif planetdata.size == "Superb": 
        pageWidth = '609.6mm'
        pageHeight = '914.4mm'
        template = 'superb.html'
        zoom = 6.20

    options = {
        'enable-local-file-access': '',
        'page-width' : pageWidth,
        'page-height' : pageHeight,
        'javascript-delay' : '1000',
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0in',
        'margin-left': '0in',
        'copies' : 1,
        'no-outline': True,
        'dpi': 96,
        'encoding': "UTF-8",
        'zoom': zoom,
    }

    selected_poster = planetdata.selected_poster
    html_content = re.sub("(<!--.*?-->)", "", planetdata.solarsystem_content.replace('vmin','em').replace('flex', '-webkit-box'), flags=re.DOTALL)

    # if selected_poster == 'whole_black' or  selected_poster == 'black_circled' or selected_poster == 'Galaxy' or selected_poster == 'multicolor':
    #     with open(os.path.join(settings.BASE_DIR,"planet/templates/svgs/zodiac-white.svg" )) as f:
    #         newText=f.read()
    #         html_content = html_content.replace('<img src="https://cdn.shopify.com/s/files/1/0604/2884/5310/files/1600-zodiac-wheel.png?v=1678104730" class="object" id="zodiac">', newText)
    #         html_content = html_content.replace('<img src="https://cdn.shopify.com/s/files/1/0604/2884/5310/files/1600-zodiac-wheel.png?v=1678104730" class="object" id="zodiac" style="display: block;">', newText)

    # if selected_poster == 'whole_black' or selected_poster == 'Galaxy' or selected_poster == 'multicolor':
    #     with open(os.path.join(settings.BASE_DIR,"planet/templates/svgs/month-white.svg" )) as f:
    #         newText2=f.read()
    #         html_content = html_content.replace('<img src="https://cdn.shopify.com/s/files/1/0604/2884/5310/files/1600-month-wheel.png?v=1678104730" class="object" id="monthWheel">', newText2)

    # if selected_poster == 'White' or selected_poster == 'white_circled':
    #     with open(os.path.join(settings.BASE_DIR,"planet/templates/svgs/zodiac-black.svg" )) as f:
    #         newText2=f.read()
    #         html_content = html_content.replace('<img src="https://cdn.shopify.com/s/files/1/0604/2884/5310/files/1600-zodiac-wheel-black.png?v=1678172067" class="object" id="zodiac">', newText2)
    #         html_content = html_content.replace('<img src="https://cdn.shopify.com/s/files/1/0604/2884/5310/files/1600-zodiac-wheel-black.png?v=1678172067" class="object" id="zodiac" style="display: block;">', newText2)
    
    # if selected_poster == 'White':
    #     with open(os.path.join(settings.BASE_DIR,"planet/templates/svgs/month-black.svg" )) as f:
    #         newText2=f.read()
    #         html_content = html_content.replace('<img src="https://cdn.shopify.com/s/files/1/0604/2884/5310/files/1600-month-wheel-black.png?v=1678175480" class="object" id="monthWheel">', newText2)

    # if selected_poster == 'black_circled':
    #     with open(os.path.join(settings.BASE_DIR,"planet/templates/svgs/month-inner-white.svg" )) as f:
    #         newText2=f.read()
    #         html_content = html_content.replace('<img src="https://cdn.shopify.com/s/files/1/0604/2884/5310/files/1600-month-wheel-black-inner-white.png?v=1678175479" class="object" id="monthWheel">', newText2)

    # if selected_poster == 'white_circled':
    #     with open(os.path.join(settings.BASE_DIR,"planet/templates/svgs/month-inner-black.svg" )) as f:
    #         newText2=f.read()
    #         html_content = html_content.replace('<img src="https://cdn.shopify.com/s/files/1/0604/2884/5310/files/1600-month-wheel-white-inner-black.png?v=1678175480" class="object" id="monthWheel">', newText2)

    # if planetdata.design == "Gold Planets":
    #     with open(os.path.join(settings.BASE_DIR,"planet/templates/svgs/month-gold.svg" )) as f:
    #         newText2=f.read()
    #         html_content = html_content.replace('<img src="https://cdn.shopify.com/s/files/1/0604/2884/5310/files/1600-month-wheel-gold-on-black-background.png?v=1678175480" class="object" id="monthWheel">', newText2)

    #     with open(os.path.join(settings.BASE_DIR,"planet/templates/svgs/zodiac-gold.svg" )) as f:
    #         newText2=f.read()
    #         html_content = html_content.replace('<img src="https://cdn.shopify.com/s/files/1/0604/2884/5310/files/1600-zodiac-wheel-gold.png?v=1678174186" class="object" id="zodiac">', newText2)
    #         html_content = html_content.replace('<img src="https://cdn.shopify.com/s/files/1/0604/2884/5310/files/1600-zodiac-wheel-gold.png?v=1678174186" class="object" id="zodiac" style="display: block;">', newText2)
    
    html_content = html_content.replace('productmedia_frame-hanger-darkwood','productmedia_frame-metal-black')
    html_content = html_content.replace('productmedia_frame-hanger-naturalwood','productmedia_frame-metal-black')
    html_content = html_content.replace('productmedia_frame-hanger-black','productmedia_frame-metal-black')
    html_content = html_content.replace('productmedia_frame-hanger-white','productmedia_frame-metal-black')
    


        
        

    context = {
        'solarsystem_content': html_content,
        'selected_poster':planetdata.selected_poster,
    }
    
    file_path = os.path.join(settings.MEDIA_ROOT, "pdf",str(planetdata.id)+".pdf")
    img_path = os.path.join(settings.MEDIA_ROOT, "pdf",str(planetdata.id)+".jpg")
    temp_pdf = loader.get_template(template)
    html_data = temp_pdf.render(context=context)
    pdf = pdfkit.from_string(html_data, file_path, options=options)

    pages = convert_from_path(file_path, 300)
    for page in pages:
        page.save(img_path, 'JPEG')
        break
    print("file uploaded")

def convert_html_to_pdf(request):
    if request.method == 'POST':

        entry_id = 115
        planetdata = get_object_or_404(PlanetData, id=entry_id)

        if planetdata.size == "Starter":
            pageWidth = '304.8mm'
            pageHeight = '406.4mm'
            template = 'starter.html'
            zoom = 3.10

        elif planetdata.size == "Standard":
            pageWidth = '457.2mm'
            pageHeight = '609.6mm'
            template = 'standard.html'
            zoom = 4.65

        elif planetdata.size == "Superb": 
            pageWidth = '609.6mm'
            pageHeight = '914.4mm'
            template = 'superb.html'
            zoom = 6.20

        options = {
            'enable-local-file-access': '',
            'page-width' : pageWidth,
            'page-height' : pageHeight,
            'javascript-delay' : '5000',
            'margin-top': '0in',
            'margin-right': '0in',
            'margin-bottom': '0in',
            'margin-left': '0in',
            'copies' : 1,
            'no-outline': True,
            'dpi': 96,
            'encoding': "UTF-8",
            'zoom': zoom,
        }

        context = {
            'solarsystem_content': planetdata.solarsystem_content.replace('vmin','em').replace('flex', '-webkit-box'),
            'selected_poster':planetdata.selected_poster,
        }
        
        temp_pdf = loader.get_template(template)
        html_data = temp_pdf.render(context=context)
        pdf = pdfkit.from_string(html_data, None, options=options)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=output.pdf'
        response.write(pdf)
        return response

    # return HttpResponse(status=200)
    return render(request, "index1.html")