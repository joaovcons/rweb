import { createApp } from 'vue'
import MaterialList from '../vue/MaterialList.vue'
import Cabecalho from '../vue/Cabecalho.vue'
import Rodape from '../vue/Rodape.vue'


const app = createApp({
  template: `
    <body>
      <Cabecalho />
    </body>
  
    <div>
      <MaterialList />
    </div>

    <body>
      <Rodape/>
    </body>
  `,
  
  components: {
    MaterialList,
    Cabecalho,
    Rodape,
  }
});

app.mount('#roteiro')
