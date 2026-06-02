document.addEventListener('DOMContentLoaded', function () {
    let areaFoto = document.getElementById('area-foto');
    let areaBotoesFoto = document.getElementById('area-botoes-foto');
    let iptEscolherArquivo = document.getElementById('iptEscolherArquivo');
    let btnRemoverImagem = document.getElementById('btnRemoverImagem');
    let btnMaximizarImagem = document.getElementById('btnMaximizarImagem');

    let btnSelecionarLocal = document.getElementById('btnSelecionarLocal');
    let btnCancelarFundoEscuro = document.getElementById('btnCancelarFundoEscuro');
    let fundoEscuro = document.getElementById('fundoEscuro');
    let btnAvancarLocal = document.getElementById('btnAvancarLocal');

    let btnEnviar = document.getElementById('btnEnviar');
    let labelTamanhoBuraco = document.getElementById('labelTamanhoBuraco');
    const nomesTamanho = {
        1: 'Pequeno',
        2: 'Médio',
        3: 'Grande',
        4: 'Gigante',
    };
    const imagemPendenteKey = 'buracometro.imagemCadastroPendente';
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

        salvarImagemTemporaria();
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
        if (areaFoto) {
            mostrarImagem(this, areaFoto);
        }
    });

    btnEnviar
    .addEventListener('click', function () {
        let form = document.getElementById('formularioCadastroBuracos');

        if (validarCampos()) {
            sessionStorage.removeItem(imagemPendenteKey);
            form.submit();
        }
    });

    function atualizarLabelTamanho() {
        const valor = document.getElementById('iptTamanho').value;

        if (labelTamanhoBuraco) {
            labelTamanhoBuraco.innerText = nomesTamanho[valor] || 'Pequeno';
        }
    }

    document.getElementById('iptTamanho').addEventListener('input', atualizarLabelTamanho);
    atualizarLabelTamanho();

    function salvarImagemTemporaria() {
        const arquivo = iptEscolherArquivo.files[0];

        if (!arquivo) {
            return;
        }

        const leitor = new FileReader();

        leitor.onload = function (event) {
            sessionStorage.setItem(imagemPendenteKey, JSON.stringify({
                nome: arquivo.name,
                tipo: arquivo.type,
                dados: event.target.result,
            }));
        };

        leitor.readAsDataURL(arquivo);
    }

    function dataUrlParaArquivo(dataUrl, nome, tipo) {
        const partes = dataUrl.split(',');
        const binario = atob(partes[1]);
        const bytes = new Uint8Array(binario.length);

        for (let i = 0; i < binario.length; i++) {
            bytes[i] = binario.charCodeAt(i);
        }

        return new File([bytes], nome, { type: tipo });
    }

    function restaurarImagemTemporaria() {
        const imagemSalva = sessionStorage.getItem(imagemPendenteKey);

        if (!imagemSalva || iptEscolherArquivo.files.length > 0) {
            return;
        }

        try {
            const imagem = JSON.parse(imagemSalva);
            const arquivo = dataUrlParaArquivo(imagem.dados, imagem.nome, imagem.tipo);
            const arquivos = new DataTransfer();

            arquivos.items.add(arquivo);
            iptEscolherArquivo.files = arquivos.files;

            if (previewImagem) {
                previewImagem.innerHTML = `
                    <img src="${imagem.dados}" alt="Prévia da imagem">
                `;
            }

            if (btnRemoverImagem) {
                btnRemoverImagem.classList.remove('oculto');
            }
        } catch (error) {
            sessionStorage.removeItem(imagemPendenteKey);
        }
    }

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

    let titulo      = iptTitulo.value;
    let coordenadas = iptCoordenadas.value;
    let endereco    = iptEndereco.value;
    let tamanho     = iptTamanho.value;
    let imagem      = iptImagem.files[0];

    if (titulo.trim() == '') {
        alert('O título não pode estar vazio!');
        return false;
    }

    if (coordenadas.trim() == '' || endereco.trim() == '') {
        alert('Selecione um local antes de prosseguir!');
        return false;
    }

    if (!(parseInt(tamanho) >= 1 && parseInt(tamanho) <= 4)) {
        alert('Tamanho inválido!');
        return false;
    }

    if (!imagem) {
        alert('Selecione uma imagem antes!');
        return false;
    }

    return true;
}

const inputImagem = document.getElementById("iptEscolherArquivo");
const previewImagem = document.getElementById("previewImagem");

function limparPreviewImagem() {
    if (inputImagem) {
        inputImagem.value = '';
    }

    if (previewImagem) {
        previewImagem.innerHTML = `
            <i class="fa-solid fa-image"></i>
            <span>Escolher imagem</span>
        `;
    }

    if (btnRemoverImagem) {
        btnRemoverImagem.classList.add('oculto');
    }

    sessionStorage.removeItem(imagemPendenteKey);
}

if (inputImagem && previewImagem) {
    inputImagem.addEventListener("change", function () {
        const arquivo = this.files[0];

        if (arquivo) {
            const leitor = new FileReader();

            leitor.onload = function (e) {
                previewImagem.innerHTML = `
                    <img src="${e.target.result}" alt="Prévia da imagem">
                `;
            };

            leitor.readAsDataURL(arquivo);
            salvarImagemTemporaria();

            if (btnRemoverImagem) {
                btnRemoverImagem.classList.remove('oculto');
            }
        } else {
            limparPreviewImagem();
        }
    });

    if (btnRemoverImagem) {
        btnRemoverImagem.addEventListener('click', limparPreviewImagem);
    }

    restaurarImagemTemporaria();
}
});
