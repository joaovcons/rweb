<!-- Template html -->

<template>
  <div class="app-container">
    <div class="content">
      <div class="material-list-container">
        <h1>Roteiro Web</h1>
        <!-- Itera sobre cada grupo de materiais -->
        <div v-for="(grupoPorPrograma, programa) in materiaisPorPrograma" :key="programa">

          <!-- Exibe o nome do programa -->
          <h2>{{ programa }}</h2>

          <!-- Itera sobre cada grupo de materiais dentro do grupo por programa -->
          <div v-for="(grupoPorPT, pt) in grupoPorPrograma" :key="pt" class="conteiner-pt">

            <div class="pt-header">
              <h3>{{ pt }}</h3>
              <img src="C:\Users\joaorc\Desktop\roteiroweb\setup\static\src\img\novo.png" @click="criarNovoMaterial(programa, pt)" class="botao-material">
              
            </div>

            <!-- Exibe a duração total do grupo por PT -->
            <h3>Duração PT: {{ calcularDuracaoPT(grupoPorPT) }}</h3>
            
            <!-- Itera sobre os materiais dentro do grupo por PT -->
      
            <div :list="grupoPorPT">
              <div v-for="(material, index) in grupoPorPT" :key="material.id" class="material-item"
              :class="{
                'green-background': material.exibicao === 'R' && material.retranca != 'FADE',
                'yellow-background': material.tipo === 'PT' && material.exibicao === 'M',
                'fade': material.cm === 'CM000000',
                'choque': index > 0 && material.choques && material.choques.length > 0 &&
                          ((material.choques.includes(grupoPorPT[index - 1].choques) && 
                          grupoPorPT[index - 1].choques.length > 0) || 
                          (index < grupoPorPT.length - 1 && material.choques.includes(grupoPorPT[index + 1].choques) && 
                          grupoPorPT[index + 1].choques.length > 0)),                   
              }">
              <p class="column-10">{{ material.exibicao }}</p>
              <p class="column-10">{{ material.cm }}</p>
              <h3 class="retranca" @click="irParaDetalhesDoMaterial(material.id)">
                {{ material.retranca }}
              </h3>

              <p class="column-10">{{ material.duracao }}</p>
              <p class="column-10">{{ material.tipo }}</p>
              <img src="C:\Users\joaorc\Desktop\roteiroweb\setup\static\src\img\editar.png" @click="editarMaterial(material.id)" class="botao-material">
              <img src="C:\Users\joaorc\Desktop\roteiroweb\setup\static\src\img\deletar.png" @click="deletarMaterial()" class="botao-material">
              <!-- icone de comentario habilitaria se o objeto tiver comentado de fato -->
              <!-- icone de avisos habilitaria se o objeto tiver avisos -->
            </div>
          </div>
          </div>
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
      materiais: [],  // Array para armazenar os materiais
      materiaisOrdenados: [],
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
    editarMaterial(materialId) {
      window.location.href = `/editar/${materialId}/`;
    },

    deletarMaterial() {
      console.log("Deletar");
    },

    comentarMaterial() {
      console.log("Comentar");
    },
    irParaDetalhesDoMaterial(materialId) {
      // Redireciona para a página de detalhes do material
      window.location.href = `/material/${materialId}/`;
    },

    atualizarGrupoPorPT(newValue) {
    this.materiaisPorPrograma[programa][pt] = newValue;
    },

    async carregarMateriais() {
      // Faz uma requisição HTTP para a API do Django para obter os materiais
      try {
        const response = await fetch('/api/materiais/');
        this.materiais = await response.json();
        this.materiaisOrdenados = [...this.materiais];
      } catch (error) {
        console.error('Erro ao carregar materiais:', error);
      }
    },

    calcularDuracaoPT(grupoPorPT) {
      let duracaoPT = 0;
      grupoPorPT.forEach(material => {
        duracaoPT += material.duracao;
      });
      return this.formatarDuracao(duracaoPT);
    },
    
    formatarDuracao(segundos) {
      const minutos = Math.floor(segundos / 60);
      const segundosRestantes = segundos % 60;

      if (segundosRestantes < 10) {
        if (minutos != 0){
        return `${minutos}'0${segundosRestantes}''`
      }
        else{
          return `${segundosRestantes}''`
        }
      }

      if (minutos != 0){
        return `${minutos}'${segundosRestantes}''`
      }
      else{
        return `${segundosRestantes}''`
      }
      ;
    },


    async criarNovoMaterial(programa, pt) {
      try {
        // Dados do novo material
        const novoMaterial = {
          cm: 'CM000000',
          retranca: 'TESTE',
          duracao: 15,
          tipo: 'CP',
          cliente: '',
          choques: '',
          exibicao: 'L',
          data: '',
          pt: pt,
          programa: programa
        }
        console.log(programa,pt)

        // Requisição para enviar os dados do novo material para o servidor
        const response = await fetch('/api/criar-material/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(novoMaterial)
        });
        console.log(novoMaterial)
        if (response.ok) {
          console.log('Novo material criado com sucesso!');
        } else {
          // Se a resposta não estiver ok, lança um erro
          throw new Error('Erro ao criar novo material');
        }
      } catch (error) {
        console.error('Erro ao criar novo material:', error);
      } finally {
        // Independentemente do resultado, atualiza os materiais após a criação ou em caso de erro
        await this.atualizarMateriais();
      }
    },

    async atualizarMateriais() {
      try {
        // Faz uma requisição HTTP para obter novamente os materiais do banco de dados
        const response = await fetch('/api/materiais/');
        
        // Verifica se a resposta da requisição está ok
        if (response.ok) {
          // Atualiza a variável 'materiais' com os dados obtidos da resposta
          this.materiais = await response.json();
          console.log('Materiais atualizados com sucesso!');
        } else {
          // Se a resposta não estiver ok, lança um erro
          throw new Error('Erro ao obter materiais');
        }
      } catch (error) {
        console.error('Erro ao atualizar materiais:', error);
      }
    }

  },
  
  mounted() {
    // Carrega os materiais ao montar o componente
    this.carregarMateriais();
  },
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
  white-space: nowrap;
}

h4 {
  font-family: "Poppins", sans-serif;
  font-weight: 500;
  text-indent: 5%;
}

p {
  font-family: "Poppins", sans-serif;
  font-size: small;
  display: flex;
  flex-direction: column;
}

.app-container{
  min-width: 50%;
  max-width: 80%;
}

.content{
  display: flex;
  justify-content: center;
}

.conteiner-pt{
  display: flex;
  flex-direction: column;
}

.pt-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 10px;

}

.botao-material { 
    cursor: pointer;
}

.popUp {
  display: none; /* Por padrão, o pop-up estará oculto */
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  border: 1px solid #ccc;
  padding: 20px;
  z-index: 999; /* Para garantir que o pop-up esteja na frente de outros elementos */
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
  border-radius: 10px;
}


.retranca {
  flex: 1 1 50%;
  cursor: pointer; 
  color: #007bff; 
  text-indent: 5px;
  text-decoration: underline; 
  padding: 3px;
 
  min-width: 50%;
  max-width: 50%;
}

.column-10 {
  flex: 1 1 1rem;
  align-items: center;
  justify-content: flex-start;
  padding: 3px;
  white-space: nowrap;
  max-width: 6%;
}
.cliente {
  flex: 1 1 1rem;
  align-items: center;
  justify-content: flex-start;
  padding: 3px;

  white-space: nowrap;
  max-width: 300px;
}


.material-title {
  cursor: pointer; 
  color: #007bff; 
  text-decoration: underline; 
}

.green-background {
  background-color: rgb(137, 239, 137); 
}

.yellow-background{
  background-color: rgb(254, 254, 109);
}
.fade{
  background-color: rgb(197, 197, 197);

}

.choque{
  background-color: rgb(255, 92, 92);
}

</style>
