from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Material
from .serializers import MaterialSerializer
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class MaterialListView(APIView):
    def get(self, request):
        materiais = Material.objects.all()
        serializer = MaterialSerializer(materiais, many=True)
        return Response(serializer.data)

class MaterialDetailView(APIView):
    def get(self, request, pk):
        material = Material.objects.get(pk=pk)
        serializer = MaterialSerializer(material)
        return Response(serializer.data)

@csrf_exempt
def adicionar_materiais(request):
    if request.method == 'POST':
        # Recebe o objeto JSON da solicitação POST
        data = json.loads(request.body)

        # Verifica se o JSON contém uma lista de materiais
        if isinstance(data, list):
            # Itera sobre cada objeto no JSON e cria um novo Material
            for material_data in data:
                material = Material.objects.create(
                    cm=material_data['cm'],
                    retranca=material_data['retranca'],
                    duracao=material_data['duracao'],
                    tipo=material_data['tipo'],
                    cliente=material_data['cliente'],
                    choques=material_data['choques'],
                    exibicao=material_data['exibicao'],
                    data=material_data['data'],
                    pt=material_data['pt'],
                    programa=material_data['programa'],
                    # Adicione outros campos conforme necessário
                )
                material.save()

            return JsonResponse({'mensagem': 'Materiais adicionados com sucesso'}, status=201)
        else:
            return JsonResponse({'erro': 'O JSON deve conter uma lista de materiais'}, status=400)
    else:
        return JsonResponse({'erro': 'Apenas solicitações POST são suportadas'}, status=400)

def index(request):
    return render(request, "index.html")