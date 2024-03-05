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
from django.db.models import Sum

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

            # Processa os materiais após adicioná-los ou atualizá-los
            processar_materiais()

            excluir_fade_local()

            return JsonResponse({'mensagem': 'Materiais adicionados com sucesso'}, status=201)
        else:
            return JsonResponse({'erro': 'O JSON deve conter uma lista de materiais'}, status=400)
    else:
        return JsonResponse({'erro': 'Apenas solicitações POST são suportadas'}, status=400)

def processar_materiais():
    # Agrupa os materiais por 'pt' e 'programa' e calcula a soma da duração para cada grupo
    materiais_agrupados = Material.objects.values('pt', 'programa').annotate(duracao_total=Sum('duracao'))
    for grupo in materiais_agrupados:
        # Recupera os materiais do grupo
        materiais_grupo = Material.objects.filter(pt=grupo['pt'], programa=grupo['programa'])
        # Verifica se há materiais com exibicao = 'L' ou 'M' no grupo e que não são o Fade Local
        materiais_exibicao = materiais_grupo.filter(exibicao__in=['L', 'M']).exclude(cm='CM000000')
        if materiais_exibicao.exists():
            # Calcula a soma da duração dos materiais com exibição 'L' ou 'M'
            duracao_total_exibicao = materiais_exibicao.aggregate(duracao_total_exibicao=Sum('duracao'))['duracao_total_exibicao']
            # Recupera o material 'FADE' do grupo, se existir
            material_fade = materiais_grupo.filter(retranca='FADE').first()
            if material_fade:
                # Subtrai a soma da duração dos materiais com exibição 'L' ou 'M' do valor de 'duracao' do material 'FADE'
                material_fade.duracao = max(0, material_fade.duracao - duracao_total_exibicao)
                material_fade.save()

def excluir_fade_local():
    # Exclui todos os materiais com cm igual a 'CM000000'
    Material.objects.filter(cm='CM000000').delete()

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
