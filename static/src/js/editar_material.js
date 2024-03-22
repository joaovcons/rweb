document.addEventListener("DOMContentLoaded", function() {
  var form = document.getElementById("editarMaterialForm");

  form.addEventListener("submit", function(event) {
    event.preventDefault(); // Evita o comportamento padrão do formulário de recarregar a página

    // Obtém os valores dos campos do formulário
    var cmValue = document.getElementById("cm").value.trim();
    var retrancaValue = document.getElementById("retranca").value.trim();

    // Verifica se os campos não estão vazios
    // Se estiverem vazios, mantém os valores originais
    cmValue = cmValue === "" ? "{{ material.cm }}" : cmValue;
    retrancaValue = retrancaValue === "" ? "{{ material.retranca }}" : retrancaValue;

    // Atualiza os valores de material.cm e material.retranca com os novos valores
    // Aqui você pode adicionar a lógica para enviar esses valores para o servidor, armazená-los no banco de dados, etc.
    // Neste exemplo, estou apenas mostrando os valores atualizados no console
    console.log("Novo valor de material.cm:", cmValue);
    console.log("Novo valor de material.retranca:", retrancaValue);

    // Limpa os campos do formulário após a submissão
    document.getElementById("cm").value = "";
    document.getElementById("retranca").value = "";
  });
});
