# Investigação do `PytestCacheWarning`

## Sintoma reproduzido

O comando `pytest tests/ -ra --tb=short` terminou com código 0 e resultado `534 passed, 1 warning`. O warning informa que o Pytest não conseguiu criar o arquivo de cache `nodeids` sob `<repo>/.pytest_cache/` por permissão negada.

## Investigação realizada

A investigação foi somente de leitura. Foram examinados:

- existência e atributos de `.pytest_cache`;
- proprietário e ACL do diretório de cache;
- ACL do diretório raiz do checkout;
- diferença entre a identidade que criou o cache e a identidade usada na reprodução autorizada.

## Causa provável

O diretório `.pytest_cache` pertence à identidade isolada usada na primeira tentativa. Sua ACL concede controle ao proprietário isolado e a identidades administrativas, mas não concede modificação à identidade usada na reprodução autorizada. O diretório raiz do checkout possui ACL mais ampla.

Assim, a causa provável é um artefato de permissões entre dois contextos locais de execução, não uma falha dos testes nem do código de domínio. A primeira tentativa criou ou materializou o cache sob uma identidade; a segunda conseguiu executar a suíte, mas não atualizar o cache pertencente à outra identidade.

## Correções possíveis — não aplicadas

1. Recriar `.pytest_cache` em um checkout limpo usando a mesma identidade que executará o Pytest.
2. Ajustar a ACL do cache para a identidade de execução, de forma controlada.
3. Usar o runner Linux efêmero do CI, que inicia com workspace e cache pertencentes à mesma identidade.

Nenhuma correção foi aplicada. Não foram alterados testes, configuração do Pytest ou plugin de cache; o warning não foi suprimido. Remoção/recriação do cache ou alteração de ACL exigirá autorização separada, pois muda o ambiente local.
