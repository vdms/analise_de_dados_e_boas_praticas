# Como a população alfabetizada se distribui no Rio de Janeiro ao longo do tempo (2000–2022)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vdms/analise_de_dados_e_boas_praticas/blob/main/data_analysis_and_good_practices.ipynb)
[![Ver relatório](https://img.shields.io/badge/Relatório-GitHub%20Pages-blue)](https://vdms.github.io/analise_de_dados_e_boas_praticas/)

## Contexto

Este projeto analisa como a população alfabetizada se distribui entre os bairros do Rio de Janeiro ao longo de três momentos censitários: 2000, 2010 e 2022.

O foco não está apenas no crescimento total, mas em como essa população se distribui territorialmente.

## Objetivo

Investigar se a distribuição da população alfabetizada entre bairros:

- é homogênea ou concentrada em poucos territórios  
- mudou ao longo do tempo  
- apresenta padrões associados a sexo e estrutura etária  

## Resumo

- A distribuição da população alfabetizada é altamente desigual em termos de volumes absolutos entre bairros
- Essa desigualdade de volumes permanece ao longo do tempo, com sinais descritivos parciais de maior heterogeneidade nos extremos da distribuição
- A participação dos maiores bairros no total observado (medida descritiva, não ajustada por população) aumenta ao longo do período
- A composição por sexo é estável entre bairros e não explica a variação observada
- Há evidência consistente de envelhecimento da população alfabetizada

> Importante: os resultados referem-se a volumes absolutos, não sendo possível inferir desigualdade relativa de alfabetização entre bairros

## Dataset

Os dados foram obtidos a partir da plataforma Data.Rio:

<https://www.data.rio/datasets/e24e35a517be408495abbe098b6672f8/about>

Links raw dos arquivos utilizados:

- 2000: <https://raw.githubusercontent.com/vdms/analise_de_dados_e_boas_praticas/main/data/495_2000.csv>
- 2010: <https://raw.githubusercontent.com/vdms/analise_de_dados_e_boas_praticas/main/data/495_2010.csv>
- 2022: <https://raw.githubusercontent.com/vdms/analise_de_dados_e_boas_praticas/main/data/495_2022.csv>

Contêm:

- população alfabetizada por bairro  
- desagregação por sexo  
- desagregação por faixas etárias  
- três anos: 2000, 2010 e 2022  

### Limitações importantes

- diferenças na estrutura das variáveis entre anos  
- ausência de denominador populacional total por bairro  
- mudanças territoriais ao longo do tempo  

## Como executar

Você pode executar o projeto de duas formas:

### Opção 1 — Google Colab (recomendado)

- Acesse diretamente:  
<https://colab.research.google.com/github/vdms/analise_de_dados_e_boas_praticas/blob/main/data_analysis_and_good_practices.ipynb>  

- Execute as células no ambiente online  

### Opção 2 — Execução local

#### Tecnologias utilizadas

- Python 3.x  
- pandas  
- numpy  
- seaborn  
- matplotlib  
- scipy  

#### Instalação

Recomenda-se o uso de um ambiente virtual.

Instale as dependências com:

```bash
pip install pandas numpy seaborn matplotlib scipy
```

- Clone o repositório  
- Execute o notebook localmente  

## Metodologia (visão geral)

Para garantir comparabilidade:

- harmonização das faixas etárias  
- uso de interseção de bairros comuns aos três anos  
- construção de painel territorial balanceado  
- exclusão controlada de dados com valores ausentes  

A análise foi conduzida com foco em:

- distribuições (histogramas, boxplots, ECDF)  
- métricas de dispersão (CV, Gini, p90/p10)  
- análise territorial (ranking e participação)  
- composição por sexo e idade  

## Principal evidência

Distribuição da população alfabetizada por bairro (2000, 2010, 2022)

![Distribuição da população alfabetizada](https://github.com/vdms/analise_de_dados_e_boas_praticas/blob/main/images/figure_3.5.png?raw=true)

Este gráfico resume o ponto central do projeto:

- a maior parte dos bairros concentra valores relativamente baixos  
- poucos bairros apresentam volumes muito elevados  
- a cauda superior se torna mais pronunciada ao longo do tempo  

## Principais análises

### Distribuição

- forte assimetria à direita  
- presença consistente de valores extremos  
- heterogeneidade persistente entre bairros  

### Território

- poucos bairros concentram grande parte dos volumes  
- aumento da participação desses bairros no total observado (medida descritiva, não ajustada por população)  
- alta rotatividade entre os maiores bairros ao longo do tempo  

### Sexo

- proporção feminina estável (~54%)  
- baixa variação entre bairros  
- associação linear fraca com volumes totais  

### Estrutura etária

- redução da participação de jovens  
- aumento consistente da participação de idosos  
- evidência de envelhecimento da população alfabetizada  

## Conclusões

- A distribuição da população alfabetizada entre bairros é fortemente desigual em termos absolutos
- Essa estrutura se mantém ao longo do tempo, com sinais descritivos parciais de maior heterogeneidade nos extremos
- O comportamento observado é compatível com efeitos de escala territorial
- Diferenças por sexo não explicam a variação observada
- Há uma mudança demográfica clara, com envelhecimento da população alfabetizada  

## Limitações

- análise baseada em volumes absolutos  
- ausência de dados populacionais totais por bairro  
- impossibilidade de inferir desigualdade relativa de alfabetização  
- exclusão de alguns territórios para manter comparabilidade  

## Nota final

Este projeto prioriza:

- consistência metodológica  
- transparência analítica  
- alinhamento entre evidência e interpretação  

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.
