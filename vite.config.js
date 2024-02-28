import { resolve } from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';


export default defineConfig({
  plugins: [vue()],
  root: './static/src',
  base: '/static/', // Defina o base como '/static/'
  server: {
    host: 'localhost',
    port: 5173,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    extensions: ['.js', '.json', '.vue'],
    alias: {
      'vue': 'vue/dist/vue.esm-bundler.js'
    }
  },
  build: {
    outDir: resolve(__dirname, 'C:\Users\joaorc\Desktop\roteiroweb\setup\static\src'), // Caminho absoluto onde os arquivos serão armazenados
    assetsDir: '', // Diretório onde os arquivos estáticos serão servidos
    manifest: true,
    emptyOutDir: true,
    target: 'es2015',
    rollupOptions: {
      input: {
        main: './js/main.js', // Caminho para o arquivo JavaScript principal
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
});
