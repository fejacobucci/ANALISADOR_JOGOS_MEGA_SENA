# PROJETO 
    > MEGA_SENA_JOGADOR

# OBJETIVO
    > Criar um aplicativo que suba os jogos da Mega Sena anteriores que estão em xlsx para o banco de dados local postgre e, depois faça avaliações dos resultados para apresentar possíveis jogos para apostar.

# CONECXÃO
    *Banco de Dados:* POSTGRESQL
    *Usuário:* felipejacobucci
    *Senha:* F&fefe1985fedc@
    *Database:* mega_sena_base

# Métricas Desejadas
    1. Frequencia de numeros que se repetiram ao longo dos anos.
    2. Frequencia de numeros que se repetiram nos 2 últimos anos
    3. Numeros que saira na posições e a quantidade de vezes
        3.1 Posição 1, quais numeros, quantas vezes
        3.2 Posição 2, quais numeros, quantas vezes
        3.3 Posição 3, quais numeros, quantas vezes
        3.4 Posição 4, quais numeros, quantas vezes
        3.5 Posição 5, quais numeros, quantas vezes
        3.6 Posição 6, quais numeros, quantas vezes
    4. Análises Estatísticas Avançadas
        4.1 Números Quentes e Frios: Mostre as dezenas que mais saíram (hot) e as que estão há mais tempo sem aparecer (cold/atrasadas).
        4.2 Frequência de Pares e Ímpares: Permita que o usuário gere jogos que respeitem a proporção estatística mais comum (ex: 3 pares e 3 ímpares).
        4.3 Análise de Quadrantes: Divida o volante em 4 partes e mostre quais áreas do cartão costumam ser mais sorteadas.
        4.4 Soma das Dezenas: Exiba a soma total dos números de cada sorteio; a maioria dos resultados vitoriosos fica em um intervalo central (geralmente entre 150 e 220).
    5. Geradores Inteligentes (Filtros)
        5.1 Fechamentos Matemáticos: Implemente algoritmos de "desdobramento" que garantem premiações menores (quadra ou quina) se você acertar uma quantidade X de números dentro de um grupo maior.
        5.2 Surpresinha "Trend": Gera jogos baseados apenas nas dezenas com maior tendência de saída no momento.
        5.3 Filtro de Jogos Anteriores: O app deve impedir que o usuário gere uma combinação que já foi sorteada em toda a história da Mega Sena (algo que nunca aconteceu duas vezes até hoje).

# Funcionalidades Desejadas
    1. Opção de Carregar o arquivo XLSX baixado com todos os jogos da caixa no banco de dados.
    2. Analise dos dados através da informação armazenada
    3. Opção de sugestão de novos jogos com métodos diferenciados 
        3.1 Método Exemplo 1: O usuário pode optar por gerar jogos se baseando em uma das métricas apresentadas
        3.2 Método Exemplo 2: O usuário pode optar por cruzar informações de métricas para gerar sugestões de jogos.

        !!! Sugira novos métodos e implemente !!!

# Informações Importantes
    1. A quantidade de registros no arquivo XLSX ultrapassa as 500 mil linhas, a aplicação deve estar preprada para carregar essa quantidade de dados no banco de dados.
    2. As métricas e funcionalidades não precisam estar todas na mesma página, pode haver uma navegação entre as métricas seja por aba ou por menu lateral.
    3. A analise e criação do banco de dados será feita pelo Claude e ele deve estar normalizado.
    4. Para a carga de arquivos (no caso o arquivo xlsx) deve haver uma barra de progresso para acompanhar o andamento da carga.
    5. Pode utilizar bibliotecas e ferramentas que ajudem tanto na apresentação dos dados quanto na consulta e carga do banco de dados.