<!-- Template html -->

<template>
  <div class="material-list-container">
    <h1>Roteiro Web - tá puxando do MaterialList.vue</h1>
    <!-- Itera sobre cada grupo de materiais -->
    <div v-for="(grupoPorPrograma, programa) in materiaisPorPrograma" :key="programa">
      <!-- Exibe o nome do programa -->
      <h2>{{ programa }}</h2>
      <!-- Itera sobre cada grupo de materiais dentro do grupo por programa -->
      <div v-for="(grupoPorPT, pt) in grupoPorPrograma" :key="pt">
        <!-- Exibe o nome do pt -->
        <h3>{{ pt }}</h3>
        <!-- Itera sobre os materiais dentro do grupo por PT -->
        <div v-for="material in grupoPorPT" :key="material.id" class="material-item" 
        :class="{
           'green-background': material.exibicao === 'R' && material.retranca != 'FADE',
           'yellow-background': material.tipo === 'PT' && material.exibicao === 'M',
          //  Outros condicionais de formatação no futuro
         }">
          <h3 class="material-title" @click="irParaDetalhesDoMaterial(material.id)">
            {{ material.retranca }}
          </h3>
          <p>{{ material.duracao }} / {{ material.tipo }} / {{ material.cliente }}</p>
        </div>
      </div>
    </div>
  </div>
</template>






<!-- Scripts JavaScript -->

<script>
export default {
  data() {
    return {
      materiais: []  // Array para armazenar os materiais
    };
  },
  computed: {
    // Função computada para agrupar os materiais por programa e pt
    materiaisPorPrograma() {
      const grupos = {};
      // Agrupa os materiais por programa e pt
      this.materiais.forEach(material => {
        if (!grupos[material.programa]) {
          grupos[material.programa] = {};
        }
        if (!grupos[material.programa][material.pt]) {
          grupos[material.programa][material.pt] = [];
        }
        grupos[material.programa][material.pt].push(material);
      });
      return grupos;
    }
  },
  methods: {
    irParaDetalhesDoMaterial(materialId) {
      // Redireciona para a página de detalhes do material
      window.location.href = `/material/${materialId}/`;
    },
    async carregarMateriais() {
      // Faz uma requisição HTTP para a API do Django para obter os materiais
      try {
        const response = await fetch('/api/materiais/');
        this.materiais = await response.json();
      } catch (error) {
        console.error('Erro ao carregar materiais:', error);
      }
    }
  },
  mounted() {
    // Carrega os materiais ao montar o componente
    this.carregarMateriais();
  }
};
</script>





<!-- Estilos CSS -->

<style scoped>
h1 {
  font-family: "Poppins", sans-serif;
  font-weight: 600;
}

h2 {
  font-family: "Poppins", sans-serif;
  font-weight: 600;
}

h3 {
  font-family: "Poppins", sans-serif;
  font-weight: 550;
}

.material-item {
  font-family: "Poppins", sans-serif;
  font-weight: 500;
  max-height: 16px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  border: 2px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  gap: 10px;
} 

.material-title {
  cursor: pointer; /* Altera o cursor para indicar que o título é clicável */
  color: #007bff; /* Cor azul para indicar um link */
  text-decoration: underline; /* Adiciona sublinhado para indicar um link */
}

.green-background {
  background-color: rgb(137, 239, 137); /* Define o fundo como verde */
}

.yellow-background{
  background-color: rgb(254, 254, 109);
}
</style>

