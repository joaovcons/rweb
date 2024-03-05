import { createApp } from 'vue'
import MaterialList from '../vue/MaterialList.vue'

const app = createApp({
  template: `
    <div>
      <MaterialList />
    </div>
  `,
  components: {
    MaterialList
  }
});

app.mount('#app')
