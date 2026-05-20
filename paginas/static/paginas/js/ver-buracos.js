document.addEventListener('DOMContentLoaded', function () {
    let btnPesquisar = document.getElementById('btnPesquisar');
    let row = document.querySelector('.row.buracos');

    btnPesquisar
    .addEventListener('click', function () {
        let texto = document.getElementById('iptPesquisar').value.trim();
        texto = texto.toLowerCase();

        row
        .querySelectorAll('.card')
        .forEach(card => {
            let titulo = card.querySelector('.card-title').innerHTML.trim();
            titulo = titulo.toLowerCase();

            if (titulo.includes(texto) || texto == '') {
                if (card.classList.contains('oculto')) 
                    card.classList.remove('oculto');
            }
            else {
                if (!card.classList.contains('oculto')) 
                    card.classList.add('oculto');
            }
        });
    });
});