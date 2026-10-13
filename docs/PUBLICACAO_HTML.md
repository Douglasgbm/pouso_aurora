# Publicação do painel HTML

Site: https://mrc888.github.io/aurora-painel/

Repositório de hospedagem: https://github.com/MRC888/aurora-painel

GitHub Pages publica a branch main, diretório raiz, por HTTPS. A hospedagem contém apenas index.html, dados.js, img/sala.png, .nojekyll e README.md. O repositório principal de Marcelo continua privado. A estrutura do painel foi preservada.

## Atualizar depois de mudar o painel

1. No projeto, executar python exportar_painel.py se os cenários ou o simulador mudarem.
2. Conferir node tools/verificar_painel.cjs e abrir o painel para revisão visual.
3. Copiar painel/index.html e painel/dados.js para a raiz do repositório aurora-painel e painel/img/sala.png para img/sala.png.
4. Publicar o commit na main de aurora-painel. O GitHub Pages atualiza o site a partir dessa branch.
5. Aguardar o sucesso de pages build and deployment e conferir o endereço online.

Os repositórios do projeto e da hospedagem são separados: alterar só o projeto não atualiza automaticamente o site. A publicação inicial de 13/10/2026 utiliza os mesmos bytes de HTML, dados e imagem do projeto revisado.
