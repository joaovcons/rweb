import { createApp } from 'vue';
import TestComponent from '../vue/Test.vue';

// Crie uma instância do aplicativo Vue
const app = createApp({
  template: '<TestComponent />',
  components: {
    TestComponent
  }
});

// Monte o aplicativo Vue dentro do elemento #app
app.mount('#app');
