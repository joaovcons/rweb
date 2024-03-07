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
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

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

@csrf_exempt # talvez isso aqui precise tirar em algum momento por questões de segurança

def adicionar_materiais(request):
    if request.method == 'POST':
        # Recebe o objeto JSON da solicitação POST
        data = json.loads(request.body)

        # Verifica se o JSON contém uma lista de materiais
        if isinstance(data, list):
            for material_data in data:
                try:
                    # Verifica se um material com os mesmos valores já existe no banco de dados
                    material = Material.objects.get(
                        retranca=material_data['retranca'],
                        duracao=material_data['duracao'],
                        pt=material_data['pt'],
                        programa=material_data['programa']
                    )
                    # Atualiza o material existente com os novos dados
                    material.cm = material_data['cm']
                    material.cliente = material_data['cliente']
                    material.choques = material_data['choques']
                    material.exibicao = material_data['exibicao']
                    material.data = material_data['data']
                    # Adicione outros campos conforme necessário
                    material.save()
                except ObjectDoesNotExist:
                    # Se o material não existir, cria um novo
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

            excluir_fade_rede()
            excluir_PD()

            return JsonResponse({'mensagem': 'Materiais adicionados com sucesso'}, status=201)
        else:
            return JsonResponse({'erro': 'O JSON deve conter uma lista de materiais'}, status=400)
    else:
        return JsonResponse({'erro': 'Apenas solicitações POST são suportadas'}, status=400)

def index(request):
    return render(request, "index.html")

def material_detail(request, pk):
    material = Material.objects.get(pk=pk)
    return render(request, 'material_detail.html', {'material': material})

class MaterialListView(APIView):
    def get(self, request):
        materiais = Material.objects.all()
        serializer = MaterialSerializer(materiais, many=True)
        return Response(serializer.data)

def excluir_fade_rede():
    # Exclui todos os fades do maestro
    Material.objects.filter(cm='FADE').delete()
    Material.objects.filter(cm='FADER').delete()
    Material.objects.filter(cm='FADER1').delete()

def excluir_PD():
    # Exclui todos os materiais com tipo vazio (ou seja, PD)
    Material.objects.filter(tipo='').delete()
