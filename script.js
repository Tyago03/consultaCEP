function consultarCEP() {
    var cep = document.getElementById('CEP').value;

    if (cep.length === 0) {
        alert('O CEP não pode ser vazio.');
        return;
    } else if (cep.length !== 8) {
        alert('Um CEP contém 8 dígitos.');
        return;
    }

    axios.get(`http://localhost:8000/cep/${cep}`)
        .then(function (response) {
            mostrarResultados(response.data);
        })
        .catch(function (error) {
            console.error('Erro na requisição: ', error);
            alert('Erro ao buscar o CEP. Verifique o console para mais detalhes.');
        });
}

function mostrarResultados(dados) {
    var tabela = document.getElementById('resultado');
    tabela.innerHTML = '';
    var linha = `<tr>
                    <td>${dados.cep}</td>
                    <td>${dados.logradouro}</td>
                    <td>${dados.complemento || ''}</td>
                    <td>${dados.bairro}</td>
                    <td>${dados.localidade}</td>
                    <td>${dados.uf}</td>
                </tr>`;
    tabela.innerHTML = linha;
}
