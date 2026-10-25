# Proteção do importador histórico contra incerteza de transcrição

Data: 2026-10-25. Estado limitado: `TRANSCRIPTION_IMPORT_GUARD_VERIFIED`.

## Problema e comportamento

O importador de avaliações históricas carregava notas e evidências ignorando metadados de incerteza de transcrição. Isso permitia consolidar uma avaliação declarada incompleta. A verificação agora ocorre antes do cálculo, da auditoria e da gravação do relatório. Nenhuma nota é alterada para acomodar o bloqueio.

Declarações pendentes, adiamentos ou incompletude bloqueiam conservadoramente a importação inteira: o importador não possui rastreabilidade suficiente para refazer parcialmente avaliações antigas. O novo fluxo de transcrição mantém seu adiamento por pergunta/resposta, documentado em [[TRANSCRIPTION_UNCERTAINTY]].

## Entradas e caminhos protegidos

- `PilotPaths` ganhou o campo opcional `transcription_review`, caminho para uma revisão JSON vinculada aos arquivos por SHA-256.
- Avaliações, evidências e entrevista estruturada configurada são inspecionadas por metadados JSON, inclusive objetos aninhados e blocos JSON em Markdown.
- `transcription_uncertainties` ou `evaluation_deferrals` não vazios, `assessment_complete: false`, tipos inválidos, JSON declarado malformado e chaves duplicadas bloqueiam a importação.
- Declarações desses campos fora de JSON suportado, incluindo YAML, bloqueiam em vez de serem ignoradas. Uma declaração JSON válida não oculta declaração conflitante em outra parte do documento.
- O arquivo de revisão precisa ter `schema_version: 1`, hashes correspondentes a todas as fontes configuradas e os três campos de completude. Arquivo ausente, esquema inválido ou hashes antigos bloqueiam.
- A revisão auxiliar não sobrepõe pendências embutidas nos arquivos. Renomear uma pendência como resolvida não a libera: não foi implementado um processo de resolução neste incremento.
- Carregadores individuais `load_individual_evaluations` e `load_evidence_set`, carregador conjunto `load_pilot_input` e geração direta `materialize_interview_evaluation_v2` verificam os metadados embutidos. O carregador conjunto e o gerador direto também recebem revisão e entrevista estruturada quando explicitamente fornecidas.

Na coordenação, o bloqueio é apresentado no gate 20.7 com prontidão falsa e diagnóstico em `artifacts.transcription_import_review`. Não há cálculo, auditoria ou novo arquivo final nesse caminho. Um relatório preexistente permanece intacto e não deve ser apresentado como resultado da execução bloqueada.

## Exemplo de revisão auxiliar

Os hashes abaixo são marcadores a preencher com SHA-256 dos bytes reais dos arquivos, não uma revisão humana pronta. O registro deliberadamente incompleto deve bloquear.

```json
{
  "schema_version": 1,
  "source_hashes": {
    "evaluations": "<hash do arquivo de avaliações>",
    "evidence": "<hash do arquivo de evidências>",
    "structured_interview": "<hash da entrevista estruturada configurada>"
  },
  "transcription_uncertainties": [
    {
      "id": "review-example",
      "status": "unresolved",
      "segment_id": "source-segment",
      "reason": "Erro identificado sem texto correto recuperável.",
      "reviewer": "<responsável pelo registro>"
    }
  ],
  "evaluation_deferrals": [],
  "assessment_complete": false
}
```

Se não houver entrevista estruturada configurada, omitir sua chave de hashes. O arquivo deve ser passado explicitamente em `PilotPaths.transcription_review`, em `load_pilot_input(..., transcription_review=...)` ou em `materialize_interview_evaluation_v2(..., transcription_review=...)`. Para essas funções diretas, fornecer também a entrevista estruturada quando aplicável (`structured_interview` no carregador e `structured_interview_path` no gerador).

## Verificação

22 métodos novos reproduziram as lacunas antes das respectivas correções. A cobertura inclui bloqueio antes da função de cálculo, preservação de saída existente, ausência de arquivo temporário, revisão desatualizada/ausente, conflitos de declaração, impossibilidade de aprovar por override e caminhos diretos. A consulta acontece antes de reutilizar execução antiga; arquivos ou revisão diferentes invalidam a reutilização por fingerprint de conteúdo.

- 80 testes direcionados aprovados.
- Regressão completa: 590/590 aprovados, sem falhas, erros ou skips.
- Reference Harness: 15/15 aprovados.
- Resultados e hashes de implementação em `TRANSCRIPTION_IMPORT_GUARD_RESULTS.json`.

Arquivos antigos sem marcações conservam o comportamento anterior. A média 4,7 no fixture histórico foi usada apenas como verificação de compatibilidade do carregamento, sem recalibração ou mudança de oracle. Fontes históricas, fórmulas de score e gates semânticos anteriores foram preservados.

## Limites e próximo passo

A ausência de marcação não demonstra fidelidade: o diagnóstico registra `fidelity_validated: false` mesmo quando a inspeção permite importar. Erros conhecidos precisam estar embutidos nos arquivos ou em uma revisão auxiliar explicitamente fornecida. O importador não procura outras conversas ou revisões pelo disco, não autentica revisores, não recupera áudio e não corrige o que o candidato disse.

Carregadores individuais só podem verificar o arquivo recebido; revisão externa e entrevista estruturada precisam ser fornecidas no carregamento conjunto ou na coordenação. Dados em memória montados por um consumidor externo que descarte marcações ficam fora desse contrato de importação.

Este checkpoint fecha a lacuna de arquivos com incerteza declarada. Entrada genérica de entrevistas/participantes e interface de revisão são os próximos incrementos; validação com uma entrevista distinta continua pendente. Não é homologação semântica geral.
