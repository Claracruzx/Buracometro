document.addEventListener('DOMContentLoaded', function () {
    let areaFoto = document.getElementById('area-foto');
    let areaBotoesFoto = document.getElementById('area-botoes-foto');
    let iptEscolherArquivo = document.getElementById('iptEscolherArquivo');
    let btnMaximizarImagem = document.getElementById('btnMaximizarImagem');

    let btnSelecionarLocal = document.getElementById('btnSelecionarLocal');
    let btnCancelarFundoEscuro = document.getElementById('btnCancelarFundoEscuro');
    let fundoEscuro = document.getElementById('fundoEscuro');
    let btnAvancarLocal = document.getElementById('btnAvancarLocal');

    let btnEnviar = document.getElementById('btnEnviar');
    // let areaMapaOculto = document.getElementById('areaMapaOculto');
    // let mapa = document.getElementById('mapa');
    // var map = L.map('mapa').setView([-2.5184, -44.2054], 16);

    let defaultMaps = document.querySelectorAll('.default-map');

    btnSelecionarLocal
    .addEventListener('click', function () {
        let form = document.getElementById('formPassandoDados');
        let titulo    = document.getElementById('iptTitulo').value;
        let descricao = document.getElementById('iptDescricao').value;
        let tamanho   = document.getElementById('iptTamanho').value;

        document.getElementById('iptHiddenTitulo').value    = titulo;
        document.getElementById('iptHiddenDescricao').value = descricao;
        document.getElementById('iptHiddenTamanho').value  = tamanho;

        form.submit();
    });

    // btnSelecionarLocal
    // .addEventListener('click', function () {
    //     fundoEscuro.classList.remove('oculto');
    //     areaMapaOculto.classList.remove('oculto');
    // });

    // btnCancelarFundoEscuro
    // .addEventListener('click', function () {
    //     fundoEscuro.classList.add('oculto');
    //     areaMapaOculto.classList.add('oculto');
    // });

    // btnAvancarLocal
    // .addEventListener('click', function () {

    // });

    iptEscolherArquivo
    .addEventListener('change', function () {
        mostrarImagem(this, areaFoto);
    });

    btnEnviar
    .addEventListener('click', function () {
        let form = document.getElementById('formularioCadastroBuracos');

        if (validarCampos()) {
            form.submit();
        }
    })

    // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    // }).addTo(map);

    // L.marker([-2.5184, -44.2054] ).addTo(map)
    //     .bindPopup("Aqui está o ponto!")
    //     .openPopup();

    // var bounds = [
    //     [-2.4025, -43.8717], // Coordenada sudoeste
    //     [-2.8044, -44.5679]  // Coordenada nordeste
    // ];

    // map.setMaxBounds(bounds);

    function mostrarImagem(input, container) {
        if (input.files && input.files[0]) {
            let reader = new FileReader();

            let style = [];
            style.push("max-width: 100%")
            style.push("max-height: 100%")
            style.push("object-fit: contain");

            reader.onload = function(e) {
                container.innerHTML = `<img src="${e.target.result}" style="${style.join(';') + ";"}">`;
                // container.innerHTML = `<img src="${e.target.result}" style="width: 100%;max-width: 100%;max-height: 100%;object-fit: contain;">`;
            };

            reader.readAsDataURL(input.files[0]);
        }
    }

    function validarCampos () {
        let iptTitulo = document.getElementById('iptTitulo');
        let iptCoordenadas = document.getElementById('iptCoordenadas');
        let iptEndereco = document.getElementById('iptEndereco');
        let iptTamanho  = document.getElementById('iptTamanho');
        let iptImagem   = document.getElementById('iptEscolherArquivo');

        let retorno = false;
        let msg = '';

        let titulo      = iptTitulo.value;
        let coordenadas = iptCoordenadas.value;
        let endereco    = iptEndereco.value;
        let tamanho     = iptTamanho.value;
        let imagem      = iptImagem.value;

        if (titulo.trim() == '') {
            msg = 'O título não pode estar vazio!';
        }
        else if (coordenadas.trim() == '' || endereco.trim() == '') {
            msg = 'Selecione um local antes de prosseguir!';
        }
        else if (!(parseInt(tamanho) >= 1 && parseInt(tamanho) <= 4)) {
            msg = 'Tamanho inválido';
        }
        else if (imagem == '') {
            msg = 'Selecione uma imagem antes';
        }
        else {
            retorno = true;
        }

        if (retorno == false) 
            alert(msg);

        return retorno;
    }
});