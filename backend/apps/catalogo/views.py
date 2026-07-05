import os
import json
import tempfile
from google import genai
from .chroma_client import search_similar_barbies
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Barbie, BarbieImage
from .serializers import BarbieSerializer, BarbieImageSerializer

class BarbieViewSet(viewsets.ModelViewSet):
    queryset = Barbie.objects.all().order_by('-created_at')
    serializer_class = BarbieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['collection', 'release_year', 'manufacturer', 'barbie_type', 'is_favorite', 'in_box']
    search_fields = ['name', 'description', 'notes', 'collection', 'manufacturer', 'barbie_type']
    ordering_fields = ['name', 'release_year', 'created_at', 'acquisition_date']

class BarbieImageViewSet(viewsets.ModelViewSet):
    queryset = BarbieImage.objects.all()
    serializer_class = BarbieImageSerializer

class StatisticsView(APIView):
    def get(self, request):
        total = Barbie.objects.count()
        in_box = Barbie.objects.filter(in_box=True).count()
        out_of_box = total - in_box
        in_box_pct = (in_box / total * 100) if total > 0 else 0
        out_of_box_pct = (out_of_box / total * 100) if total > 0 else 0

        collections = Barbie.objects.values('collection').annotate(count=Count('id')).order_by('-count')
        manufacturers = Barbie.objects.values('manufacturer').annotate(count=Count('id')).order_by('-count')
        types = Barbie.objects.values('barbie_type').annotate(count=Count('id')).order_by('-count')

        # Decades logic
        decades = {}
        for barbie in Barbie.objects.filter(release_year__isnull=False):
            decade = (barbie.release_year // 10) * 10
            decades[decade] = decades.get(decade, 0) + 1
        
        return Response({
            'total_barbies': total,
            'in_box_count': in_box,
            'out_of_box_count': out_of_box,
            'in_box_percentage': in_box_pct,
            'out_of_box_percentage': out_of_box_pct,
            'by_collection': collections,
            'by_manufacturer': manufacturers,
            'by_type': types,
            'by_decade': decades,
        })

class VisionAnalysisView(APIView):
    def post(self, request):
        images = request.FILES.getlist('images')
        
        if not images:
            return Response({"error": "No se subieron imágenes."}, status=400)

        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            return Response({
                "inferred": {
                    "name": "Barbie (Mock AI)",
                    "hair_color": "Rubio",
                    "eye_color": "Azul",
                    "collection": "Fashionistas",
                    "release_year": "2023",
                    "notes": "Falta API Key."
                }
            })

        try:
            client = genai.Client(api_key=api_key)
            uploaded_files = []
            
            # 1. Guardar temporalmente las imágenes y subirlas a Gemini
            for img in images:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                    for chunk in img.chunks():
                        temp_file.write(chunk)
                    temp_file_path = temp_file.name
                
                # Subir el archivo temporal a Gemini
                gemini_file = client.files.upload(file=temp_file_path)
                uploaded_files.append(gemini_file)
                
                # Eliminar el archivo local temporal
                os.remove(temp_file_path)

            # 2. RAG - Paso 1: Pedir a Gemini una descripción básica visual para buscar en ChromaDB
            description_prompt = "Describe detalladamente esta muñeca Barbie (ropa, color de pelo, estilo) en una sola frase para buscar en una base de datos."
            desc_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[description_prompt] + uploaded_files,
            )
            visual_description = desc_response.text
            
            # 3. RAG - Paso 2: Buscar en ChromaDB Barbies similares de la colección del usuario
            similar_barbies = search_similar_barbies(visual_description, n_results=3)
            context_text = "No hay muñecas previas similares en la colección."
            if similar_barbies:
                context_text = "Muñecas similares ya registradas en la colección del usuario:\n"
                for i, b in enumerate(similar_barbies):
                    context_text += f"{i+1}. {b['text']}\n"
            
            # 4. RAG - Paso 3: Generación final enriquecida con el contexto
            final_prompt = f"""
            Analiza esta(s) foto(s) de una muñeca Barbie y devuelve UNICAMENTE un JSON válido con los siguientes campos inferidos en español:
            name, collection, release_year, manufacturer, barbie_type, hair_color, eye_color, dress_color, condition, notes, in_box (booleano).
            
            IMPORTANTE - CONTEXTO RAG:
            {context_text}
            
            Si la muñeca de la foto parece ser la misma o de la misma colección que alguna del contexto anterior, USA EXACTAMENTE el mismo nombre de colección o convenciones de nombres.
            Devuelve SOLO el JSON, sin formato markdown (sin ```json).
            """
            
            final_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[final_prompt] + uploaded_files,
            )
            
            # Limpiar posible markdown del JSON
            text_response = final_response.text.replace('```json', '').replace('```', '').strip()
            inferred_data = json.loads(text_response)

            return Response({
                "inferred": inferred_data
            })
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

