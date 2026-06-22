# Nota de Conformidade e Ética de Dados

## Sobre a coleta

Os dados de restaurantes utilizados neste projeto foram coletados de forma manual a partir
da interface pública do iFood, acessível a qualquer usuário do aplicativo, exclusivamente
para fins de pesquisa acadêmica e construção de portfólio. Nenhum dado foi obtido mediante
automação em escala, burla de mecanismos de segurança ou acesso a áreas restritas.

## Dados brutos não versionados

Os arquivos brutos da coleta (respostas JSON da API interna do iFood) **não são incluídos
neste repositório**, pelas seguintes razões:

1. **Termos de uso:** os dados pertencem ao iFood e a seus restaurantes parceiros. A
   redistribuição pública desses dados não é autorizada.
2. **LGPD:** embora os dados sejam de estabelecimentos comerciais (e não de pessoas físicas),
   adota-se postura conservadora, evitando a republicação de qualquer informação operacional
   de terceiros (preços, identificadores internos, dados de entrega).
3. **Boas práticas:** o repositório versiona apenas dados **agregados e anonimizados** no nível
   de distrito, suficientes para reprodutibilidade analítica sem expor dados primários.

## O que é versionado

- Dados **agregados por distrito** (percentuais de cobertura), sem identificação de
  restaurantes individuais.
- Dados socioeconômicos de **fonte pública oficial** (Mapa da Desigualdade 2024, Rede Nossa SP).
- Todo o código de processamento e análise.

## Finalidade

Este é um projeto de **pesquisa e portfólio**, sem fim comercial. A análise busca evidenciar
um padrão de desigualdade no acesso a benefícios alimentares, com potencial valor para
políticas públicas e para a própria plataforma. Não há intenção de prejudicar o iFood,
os restaurantes ou as operadoras de VR mencionadas.

## Reprodutibilidade

O método de coleta está documentado em `docs/METODOLOGIA.md`. Qualquer pessoa pode reproduzir
a coleta seguindo o procedimento descrito, gerando seus próprios dados brutos localmente.
