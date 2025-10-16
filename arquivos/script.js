document.addEventListener('DOMContentLoaded', () => {
  const formCadastrar = document.getElementById('form-cadastrar');
  const tabelaClientes = document.getElementById('tabela-clientes').querySelector('tbody');

  // Coloque aqui sua URL do crudcrud (atenção: expira depois de um tempo)
  const API_URL = 'https://crudcrud.com/api/36fc9991e12d4e19bb3a1ddaae443d0a/clientes';

  const listarClientes = async () => {
    try {
      const res = await fetch(API_URL);
      if (!res.ok) throw new Error('Erro ao buscar clientes');
      const clientes = await res.json();

      tabelaClientes.innerHTML = '';
      clientes.forEach(cliente => {
        const tr = document.createElement('tr');

        const tdNome = document.createElement('td');
        tdNome.textContent = cliente.nome || '';
        tr.appendChild(tdNome);

        const tdEmail = document.createElement('td');
        tdEmail.textContent = cliente.email || '';
        tr.appendChild(tdEmail);

        const tdAcoes = document.createElement('td');
        const btnExcluir = document.createElement('button');
        btnExcluir.textContent = 'Excluir';
        btnExcluir.addEventListener('click', () => excluirCliente(cliente._id));
        tdAcoes.appendChild(btnExcluir);
        tr.appendChild(tdAcoes);

        tabelaClientes.appendChild(tr);
      });
    } catch (err) {
      console.error('Erro:', err);
    }
  };

  formCadastrar.addEventListener('submit', async (e) => {
    e.preventDefault();
    const nome = document.getElementById('nome').value.trim();
    const email = document.getElementById('email').value.trim();

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, email })
      });
      if (!res.ok) throw new Error('Erro ao cadastrar cliente');

      formCadastrar.reset();
      listarClientes();
    } catch (err) {
      console.error('Erro:', err);
    }
  });

  window.excluirCliente = async (id) => {
    try {
      const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Erro ao excluir cliente');
      listarClientes();
    } catch (err) {
      console.error('Erro:', err);
    }
  };

  listarClientes();
});
