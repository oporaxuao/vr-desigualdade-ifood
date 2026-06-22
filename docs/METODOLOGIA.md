# Metodologia de Coleta e Análise

## 1. Desenho da pesquisa

Estudo observacional de corte transversal, com amostragem estratificada por quartil de renda.
Unidade de análise: restaurante acessível a partir do distrito.

## 2. Seleção dos distritos

Os 40 distritos foram selecionados a partir do ranking de **Trabalho e Renda** do
Mapa da Desigualdade 2024 (Rede Nossa São Paulo), que classifica os 96 distritos do
município. A seleção garantiu **10 distritos por quartil**:

- **Q1 (alta renda):** posições 1–24 do ranking
- **Q2 (média-alta):** posições 25–48
- **Q3 (média-baixa):** posições 49–72
- **Q4 (baixa renda):** posições 73–96

A seleção cobriu também as cinco zonas geográficas da cidade (Centro, Norte, Sul, Leste, Oeste).

## 3. Procedimento de coleta

1. Para cada distrito, escolheu-se um endereço em via **residencial** (não comercial),
   identificado por inspeção visual no Google Maps.
2. O endereço foi inserido no iFood e capturou-se a resposta da API `HOME_FOOD_DELIVERY_V3`
   via DevTools do navegador, contendo os 20 primeiros restaurantes listados.
3. Para cada restaurante, consultou-se o endpoint `/v1/merchants/{id}/payment-methods`
   para extrair as bandeiras de VR aceitas.
4. Os dados foram processados e agregados por distrito.

## 4. Variáveis socioeconômicas

Três indicadores oficiais de Trabalho e Renda por distrito (Mapa da Desigualdade 2024):

- Remuneração média mensal do emprego formal (R$)
- Oferta de emprego formal
- Desigualdade salarial no emprego formal

## 5. Tratamento de sobreposição entre distritos

Distritos vizinhos compartilham parte da oferta de restaurantes (mesmo raio de entrega).
Optou-se por **manter o restaurante em cada distrito de onde é acessível**, em vez de
atribuí-lo a um único distrito. Justificativa: a pergunta de pesquisa é sobre a oferta
acessível ao morador de cada distrito, não sobre a localização física exclusiva do restaurante.

## 6. Limitações

- Amostra de 20 restaurantes por distrito (os primeiros listados pelo algoritmo do iFood),
  o que reflete o ranking de relevância da plataforma, não um censo completo.
- Coleta pontual (junho/2026); a cobertura de VR pode variar ao longo do tempo.
- Sem coordenadas individuais dos restaurantes (apenas do ponto de busca).
- Osasco e outros municípios da Grande SP foram excluídos por não constarem no
  Mapa da Desigualdade do município de São Paulo.

## 7. Análises estatísticas

- Correlação de Pearson entre renda e cobertura por bandeira.
- Teste qui-quadrado de independência entre quartil de renda e aceitação de cada bandeira.
- Modelo preditivo (XGBoost) com interpretabilidade via SHAP, como complemento exploratório.
