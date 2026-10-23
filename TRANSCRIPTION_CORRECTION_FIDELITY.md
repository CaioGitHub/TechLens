# Correção fiel da transcrição — primeira integração

Data: 2026-10-23. Branch: `codex/transcription-baseline`.

## Objetivo e comportamento implementado

Receber propostas de correção lexical sem alterar automaticamente o que o candidato afirmou. O original, os intervalos das propostas e seus IDs de fonte são preservados. O contexto e um glossário fornecido pelo chamador podem sugerir um termo próximo, mas não comprovam que houve erro de reconhecimento.

O módulo `reference_runtime/transcription_correction.py` oferece proposta, aprovação explícita após conferência da fonte, rejeição e materialização. Não consulta um provedor externo de IA ou áudio. É a camada de controle e aplicação; geração semântica ampla e interface de revisão ficam em etapas posteriores.

Todas as correções lexicais ficam pendentes até revisão explícita. Aprovação exige revisor identificado, declaração de conferência da fonte, apoio contextual e elegibilidade da mudança. Números, negação, incerteza, modalidades, polaridade e marcadores de experiência são protegidos por verificações conservadoras. Completar termos interrompidos ou transformar síncrono em assíncrono não é tratado como simples reparo ortográfico.

## Integração ao fluxo existente

A reconstrução 20.5 aceita `transcription_correction_plans` por response ID. Antes de seguir, confere texto original e IDs de segmentos com a resposta real, recalcula as mudanças e anexa `correction_audit`. Propostas pendentes interrompem essa nova entrada antes da avaliação; mudanças em campos resumidos do plano não são usadas como texto final.

O caminho novo não aceita mistura com `reconstructions`, preservado para compatibilidade dos fixtures históricos. Os resultados antigos de regressão não foram reclassificados por esta implementação.

## Validação executada entre mudanças

- Dez testes de fidelidade passaram antes da ligação ao pipeline.
- Integração e regressões direcionadas: 80 testes aprovados.
- Controles adicionais de rejeição, conflito e fonte: 86 testes aprovados.
- Uma verificação adicional encontrou aplicação incorreta de ajustes sobrepostos após alteração de flags. Foi criada reprodução com falha e o cálculo passou a conferir os intervalos reais, sem confiar nas flags. Após a correção: 87 testes direcionados aprovados.
- Suíte final: **549 testes aprovados**, zero falhas, erros ou ignorados; 16.634 s.
- Reference Harness final: **15/15 aprovados**; 16.158 s.
- Hashes do runtime e do módulo de correção permaneceram inalterados durante a verificação final. Saídas reais: `TRANSCRIPTION_CORRECTION_FIDELITY_RESULTS.json`.

Há 19 novos métodos de teste de fidelidade. Os exemplos são sintéticos e não constituem referência humana independente.

## Exemplo de comportamento verificado

Original: “Eu usaria Spring Boto neste projeto.”
Proposta contextual: “Spring Boot”. Antes da revisão, o texto entregue continua original e o plano não é liberado para avaliação. Após conferência explícita da fonte e aceitação do reparo, resulta “Eu usaria Spring Boot neste projeto.” O condicional “usaria” é preservado; ele não se torna experiência demonstrada.

## Limitações e critérios ainda abertos

- Não há corretor semântico geral, ASR, carregamento automático da base técnica ou UI de revisão implementados por este checkpoint.
- Um glossário e similaridade ortográfica não provam intenção do candidato. A declaração de conferência é fornecida pelo revisor; não é autenticação criptográfica de identidade ou prova de acesso a áudio.
- As proteções lexicais são conservadoras e finitas, não equivalência semântica universal. Paráfrases amplas e recuperação de palavras realmente ausentes continuam fora da aplicação automática.
- Casos bloqueados devem ser rejeitados ou resolvidos a partir da fonte em etapa própria; não se relaxam regras para fazer uma resposta parecer correta.
- Os bloqueios históricos de validação semântica do avaliador não foram removidos.

Estado limitado: `FAITHFUL_TRANSCRIPT_REVIEW_CORE_IMPLEMENTED_AND_REGRESSION_VERIFIED`.

O plano está em `TRANSCRIPTION_IMPLEMENTATION_PLAN.md`. Próxima etapa: entrada de entrevista e revisão aplicável a transcrições reais, seguida de propostas contextuais baseadas em fontes e de testes de fidelidade revisados.
