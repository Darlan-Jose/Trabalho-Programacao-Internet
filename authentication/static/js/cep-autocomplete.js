document.addEventListener('DOMContentLoaded', function() {
    const cepField = document.getElementById('cep-field');
    const searchCepBtn = document.getElementById('search-cep-btn');
    const cepMessage = document.getElementById('cep-message');
    
    const streetField = document.getElementById('street-field');
    const neighborhoodField = document.getElementById('neighborhood-field');
    const cityField = document.getElementById('city-field');
    const stateField = document.getElementById('state-field');
    
    function searchCEP() {
        const cep = cepField.value.replace(/\D/g, '');
        
        if (cep.length !== 8) {
            showMessage('Digite um CEP válido com 8 dígitos', 'error');
            return;
        }
        
        showMessage('Buscando CEP...', 'loading');
        
        // Faz a requisição para a API do ViaCEP
        fetch(`/api/cep/${cep}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Preenche os campos com os dados retornados
                    streetField.value = data.address.street || '';
                    neighborhoodField.value = data.address.neighborhood || '';
                    cityField.value = data.address.city || '';
                    stateField.value = data.address.state || '';
                    
                    showMessage('Endereço encontrado!', 'success');
                    
                    // Foca no campo número para facilitar o preenchimento
                    document.getElementById('number-field').focus();
                } else {
                    showMessage(data.error || 'CEP não encontrado', 'error');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                showMessage('Erro ao buscar CEP. Tente novamente.', 'error');
            });
    }
    
    function showMessage(message, type) {
        cepMessage.textContent = message;
        cepMessage.className = 'mt-1';
        
        if (type === 'success') {
            cepMessage.classList.add('text-success');
        } else if (type === 'error') {
            cepMessage.classList.add('text-danger');
        } else if (type === 'loading') {
            cepMessage.classList.add('text-info');
        }
    }
    
    if (searchCepBtn) {
        searchCepBtn.addEventListener('click', searchCEP);
    }
    
    // Busca automática quando o CEP tiver 8 dígitos
    if (cepField) {
        cepField.addEventListener('input', function() {
            const cep = this.value.replace(/\D/g, '');
            if (cep.length === 8) {
                searchCEP();
            }
        });
        
        // Formata o CEP (XXXXX-XXX)
        cepField.addEventListener('input', function() {
            let cep = this.value.replace(/\D/g, '');
            if (cep.length > 5) {
                cep = cep.substring(0, 5) + '-' + cep.substring(5, 8);
            }
            this.value = cep;
        });
    }
});