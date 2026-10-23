# Piloto de revisão fiel — conjunto de referência e critérios de aceite

Data: 2026-10-23. Estado: `REFERENCE_REVIEW_PENDING`.

## Material disponível e limites

O inventário em `TRANSCRIPTION_REFERENCE_SET_MANIFEST.json` identifica três arquivos de uma única entrevista, pela data e identificação nos metadados. O texto da versão completa na pasta do piloto 05 coincide com a versão v3 na pasta do piloto 01; a v2 é uma versão parcial da mesma entrevista. Os caminhos de pasta não demonstram candidatos diferentes. Hashes de arquivo e do bloco transcrito distinguem alterações de documento e conteúdo.

O piloto usa oito trechos reais dessa entrevista. Não há correções de referência aprovadas: rótulos, substituições e revisor permanecem vazios. As transcrições existentes, inclusive campos de confiança históricos, não demonstram conferência humana nem acesso ao áudio. Não presumir erro de reconhecimento a partir de uma palavra incomum.

Uma revisão humana fundamentada pode validar trechos desta entrevista. Uma segunda entrevista distinta é requisito para ampliar a avaliação de generalização, não para iniciar ou concluir a revisão deste piloto. Versões da mesma entrevista devem permanecer no mesmo grupo de desenvolvimento/avaliação.

## Casos localizados

As linhas referem-se à fonte completa do piloto 05, fixada pelo hash no manifesto. O manifesto guarda localização e hash do trecho sem replicar a entrevista.

| Caso | Cobertura pretendida | Timestamp | Linha da fonte | Revisão |
| --- | --- | --- | --- | --- |
| REF-01 | Termo possivelmente reconhecido incorretamente | 03:49 | 101 | Pendente |
| REF-02 | Nome de produto ambíguo | 07:22 | 185 | Pendente |
| REF-03 | Negação e experiência declarada | 05:36 | 155 | Pendente |
| REF-04 | Incerteza e hipótese | 08:16 | 200 | Pendente |
| REF-05 | Números e versões | 04:05 | 119 | Pendente |
| REF-06 | Frase interrompida | 02:53 | 83 | Pendente |
| REF-07 | Afirmação técnica preservada | 04:37 | 131 | Pendente |
| REF-08 | Duração da experiência | 02:28 | 77 | Pendente |

## Procedimento incremental

1. Conferir integridade das fontes e localizar os oito trechos com o contexto dos turnos anterior e seguinte. Preservar original, atribuição de fala e timestamps.
2. O revisor registra por caso: manter, corrigir ou ambíguo; proposta; justificativa; identidade; fonte efetivamente consultada e localização da evidência. Áudio, quando disponível, deve ter seu intervalo indicado. Uma leitura do texto ou um glossário, sozinhos, não provam o que foi pronunciado.
3. Se a evidência não resolver o termo, marcar ambíguo e manter o original. Não adivinhar marcas, tecnologias ou conhecimento do candidato. Divergências entre revisores ficam abertas até resolução documentada.
4. Fixar as decisões humanas e seus hashes antes de comparar as propostas do sistema. Não ajustar a referência olhando a previsão. Se o caso já orientou desenvolvimento, identificá-lo como desenvolvimento; não apresentar como validação cega.
5. Executar proposta, aprovação/rejeição, aplicação e entrada da avaliação com as referências fixadas. Testar cada grupo de mudanças; corrigir falhas antes do grupo seguinte. Registrar diferenças e o checkpoint real.
6. Só ampliar a automação após o piloto. Acrescentar entrevista distinta e revisada para avaliar generalização, sem promover os bloqueios semânticos históricos.

## Critérios de aceite do piloto

| Critério | Evidência exigida |
| --- | --- |
| Integridade | Todos os arquivos e trechos localizados com hashes correspondentes; original recuperável integralmente. |
| Revisão completa | Oito decisões humanas registradas como manter, corrigir ou ambíguo, com revisor, justificativa e fonte consultada; casos sem evidência suficiente permanecem ambíguos. |
| Correção fiel | Toda substituição aplicada corresponde exatamente à decisão apoiada na fonte; zero acréscimos de conhecimento, experiência ou conclusão de frase. |
| Conteúdo sensível | Negação, incerteza, modalidade, quantidades, versões e atribuição de fala preservadas, ou divergência de reconhecimento explicitamente comprovada e revisada. |
| Pendências | Zero propostas pendentes encaminhadas à avaliação pela entrada revisada; rejeições e ambiguidades preservam o original e são exportadas como tais. |
| Rastreabilidade | Cada alteração aponta fonte, intervalo original, texto proposto, decisão, revisor e versão efetivamente aplicada; saídas da avaliação ligadas a essa versão. |
| Reprodutibilidade | Mesmas entradas e decisões produzem mesma versão aplicada; aprovação não altera fonte nem evidência histórica. |
| Integração | Testes do fluxo completo, regressão e harness aprovados no checkpoint que contiver implementação; divergências de avaliação explicadas sem calibrar scores para atingir o resultado. |
| Relato honesto | Informar separadamente cobertura 8/8, decisões manter/corrigir/ambíguo, substituições verificadas, erros e pendências; sem acurácia sobre casos sem referência resolvida. |

Não há requisito de transformar todos os oito casos em correções. Uma ambiguidade corretamente preservada é um resultado válido do piloto, mas não conta como correção humana verificada. Nenhum limiar de acurácia geral é inferido desta amostra pequena e conhecida.

## Próximo checkpoint

Preparar a revisão dos oito trechos com evidência da fonte. A implementação atual continua no núcleo conservador descrito em `TRANSCRIPTION_CORRECTION_FIDELITY.md`. Esta entrega é documentação e manifesto de localização, sem novas regras de correção, interface ou referências humanas fabricadas. A última regressão de implementação registrada permanece 549 testes globais e 15 do harness aprovados; não é uma nova execução deste plano.
