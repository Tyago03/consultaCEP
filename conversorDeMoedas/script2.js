document.addEventListener('DOMContentLoaded', function () {
    axios.get('http://localhost:8000/moedas')
        .then(function (response) {
            const currencies = response.data;

            if (!currencies || currencies.length === 0) {
                console.error("Erro");
                return;
            }

            const convertFrom = document.getElementById('convertFrom');
            const convertTo = document.getElementById('convertTo');

            currencies.forEach(currency => {
                const option1 = document.createElement('option');
                const option2 = document.createElement('option');
                option1.textContent = `${currency.nome} (${currency.codigo})`;
                option2.textContent = `${currency.nome} (${currency.codigo})`;
                option1.value = currency.codigo;
                option2.value = currency.codigo;

                convertFrom.appendChild(option1);
                convertTo.appendChild(option2);
            });
        })
        .catch(function (error) {
            console.error('Erro ao carregar moedas:', error);
        });
});

function convertCurrency() {
    const fromCurrency = document.getElementById('convertFrom').value;
    const toCurrency = document.getElementById('convertTo').value;
    const amount = parseFloat(document.getElementById('amount').value);

    if (isNaN(amount) || amount <= 0) {
        alert("Por favor, insira um valor válido maior que zero.");
        return;
    }

    const url = `https://economia.awesomeapi.com.br/last/${fromCurrency}-${toCurrency}`;
    
    axios.get(url)
        .then(response => {
            const currencyData = response.data;
            const key = `${fromCurrency}${toCurrency}`; // Key como USD-BRL
            const bid = currencyData[key].bid;

            const convertedAmount = (amount * parseFloat(bid)).toFixed(2);
            alert(`Convertido: ${convertedAmount} ${toCurrency}`);
        })
        .catch(error => {
            console.error('Erro ao buscar a taxa de câmbio:', error);
            alert('Houve um erro ao buscar a taxa de câmbio. Por favor, tente novamente.');
        });
}


