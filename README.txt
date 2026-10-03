# Carteira Micro EGI 3x — V4 Render + Potencial

Arquivos prontos para publicar no Render.

## Estrutura
- `app.py` — backend Flask. Faz a consulta à MEXC Futures e envia ntfy.
- `index.html` — app da carteira com Painel da Carteira.
- `requirements.txt` — dependências Python.
- `render.yaml` — configuração opcional do Render.

## Render
1. Suba estes arquivos para a raiz de um repositório GitHub.
2. No Render: New > Web Service.
3. Conecte o repositório.
4. Runtime: Python.
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn app:app`
7. Opcional: Environment > `NTFY_TOPIC` = seu tópico ntfy.
8. Deploy.

Se o `index.html` for aberto pelo próprio endereço do Render, deixe o campo "URL do backend Render" em branco.
Se abrir o HTML separado/localmente, informe nesse campo algo como:
`https://SEU-SERVICO.onrender.com`

## Teste
- Abra o app.
- Clique em `🧪 Testar Render`.
- Deve aparecer `✅ Render OK`.
- Depois clique em `🔄 Atualizar Tudo Agora`.
- Para ntfy: configure `NTFY_TOPIC` no Render ou digite o tópico no app, e clique `🔔 Testar ntfy`.

## Observação
Em plano gratuito, o serviço Render pode ficar inativo após um período sem requisições e precisar acordar na primeira chamada.


## Novo na V4 — botão Potencial / Por que comprar?
Cada moeda possui o botão `💡 Potencial / Por que comprar?`.

Ele mostra:
- potencial técnico atual (ALTO / MÉDIO / EM FORMAÇÃO / BAIXO);
- quais regras sustentam a compra;
- quais confirmações ainda faltam;
- risco estimado;
- alvos teóricos 1R, 2R e 3R quando entrada e stop estão disponíveis.

A mesma análise é anexada automaticamente ao Relatório GPT.


## V4.1 — BTC fixo no topo
- BTCUSDT fica sempre na primeira posição.
- BTC é somente REFERÊNCIA DO MERCADO; não consome margem, não conta como posição e não entra na carteira de microcaps.
- O botão `🧭 Contexto BTC` mostra se o ambiente está favorável, misto ou contrário para LONGs.
- Mudança de contexto do BTC pode gerar aviso ntfy.
- O Relatório GPT recebe uma seção `CONTEXTO BTC — REFERÊNCIA DO MERCADO` antes das microcaps.
