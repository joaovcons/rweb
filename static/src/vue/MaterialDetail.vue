<!-- MaterialDetail.vue -->

<template>
    <div>
      <h1>{{ material.retranca }}</h1>
      <p>Cliente: {{ material.cliente }}</p>
      <p>Choques: {{ material.choques }}</p>
      <!-- Adicione mais detalhes conforme necessário -->
    </div>
  </template>
  
  <script>
  export default {
    props: ['id']
  };
  </script>
  
  <style scoped>
  /* Adicione estilos conforme necessário */
  </style>
  