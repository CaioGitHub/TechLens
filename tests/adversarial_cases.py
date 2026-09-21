from copy import deepcopy


PARTICIPANTS = [
    {"participant_id": "P-ADV-CANDIDATE", "name": "Candidate Adversarial", "role": "candidate"},
    {"participant_id": "P-ADV-INTERVIEWER", "name": "Interviewer Adversarial", "role": "interviewer"},
]


def _case(case_id, transcript, **metadata):
    fixture = {
        "fixture_id": case_id,
        "pipeline_version": "29-reference-1",
        "participants": deepcopy(PARTICIPANTS),
        "raw_transcript": [
            {"id": f"{case_id}-{index:02d}", "timestamp": f"12:00:{index:02d}", **item}
            for index, item in enumerate(transcript, start=1)
        ],
    }
    fixture.update(metadata)
    return fixture


def adversarial_fixtures():
    return {
        "ADV-01": _case(
            "ADV-01",
            [
                {"speaker": "Interviewer Adversarial", "text": "Você usaria cache distribuído?"},
                {"speaker": "Candidate Adversarial", "text": "Eu usaria cache distribuído; na verdade, nesse caso eu não usaria cache porque os dados precisam ser sempre consistentes."},
            ],
        ),
        "ADV-02": _case(
            "ADV-02",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como funcionam virtual threads?"},
                {"speaker": "Candidate Adversarial", "text": "Virtual Threads criam uma thread do sistema operacional para cada request; pensando melhor, elas usam threads virtuais gerenciadas pela JVM."},
            ],
        ),
        "ADV-03": _case(
            "ADV-03",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como você escolheria Kafka ou Redis?"},
                {"speaker": "Candidate Adversarial", "text": "A princípio eu usaria Kafka; não, acho que nesse caso Redis resolveria porque Kafka não suporta mensagens."},
            ],
        ),
        "ADV-04": _case(
            "ADV-04",
            [
                {"speaker": "Interviewer Adversarial", "text": "Você concorda que seria melhor usar cache, certo?"},
                {"speaker": "Candidate Adversarial", "text": "Sim."},
                {"speaker": "Interviewer Adversarial", "text": "Porque Redis resolveria o problema?"},
                {"speaker": "Candidate Adversarial", "text": "Sim."},
            ],
        ),
        "ADV-05": _case(
            "ADV-05",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como observar requests, dependencies e exceptions?"},
                {"speaker": "Interviewer Adversarial", "text": "Você poderia usar Application Insights para observar requests, dependencies e exceptions."},
                {"speaker": "Candidate Adversarial", "text": "Exatamente."},
            ],
        ),
        "ADV-06": _case(
            "ADV-06",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como investigaria uma API lenta?"},
                {"speaker": "Candidate Adversarial", "text": "Eu resolveria olhando primeiro..."},
                {"speaker": "Interviewer Adversarial", "text": "Pode continuar."},
                {"speaker": "Candidate Adversarial", "text": "...os logs e as dependências externas."},
            ],
        ),
        "ADV-07": _case(
            "ADV-07",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como você investigaria uma API lenta?"},
                {"speaker": "Candidate Adversarial", "text": "Eu começaria pelas métricas."},
                {"speaker": "Interviewer Adversarial", "text": "E pensando em observabilidade, quais sinais você olharia?"},
                {"speaker": "Candidate Adversarial", "text": "Requests, dependencies e traces."},
            ],
        ),
        "ADV-08": _case(
            "ADV-08",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como você monitoraria uma aplicação?"},
                {"speaker": "Candidate Adversarial", "text": "Eu acompanharia métricas e logs."},
                {"speaker": "Interviewer Adversarial", "text": "E se a aplicação estiver apresentando aumento de latência?"},
                {"speaker": "Candidate Adversarial", "text": "Eu isolaria dependências e compararia com um baseline."},
            ],
        ),
        "ADV-09": _case(
            "ADV-09",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como funciona uma transação no Spring?"},
                {"speaker": "Candidate Adversarial", "text": "Virtual threads são leves e gerenciadas pela JVM."},
            ],
        ),
        "ADV-10": _case(
            "ADV-10",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como você desenharia essa arquitetura?"},
                {"speaker": "Candidate Adversarial", "text": "Eu aplicaria DDD, SOLID, CQRS, event sourcing, hexagonal e observabilidade distribuída."},
            ],
        ),
        "ADV-11": _case(
            "ADV-11",
            [
                {"speaker": "Interviewer Adversarial", "text": "O que é injeção de dependência?"},
                {"speaker": "Candidate Adversarial", "text": "É um conceito importante e bastante utilizado. Em muitos sistemas modernos, equipes maduras aplicam boas práticas para manter o código organizado, sustentável e preparado para mudanças. Isso ajuda a construir software melhor e facilita a manutenção ao longo do tempo."},
            ],
        ),
        "ADV-12": _case(
            "ADV-12",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como você configuraria managed identity?"},
                {"speaker": "Candidate Adversarial", "text": "Eu usaria managed identity para evitar credenciais armazenadas e aplicaria apenas o RBAC necessário."},
            ],
        ),
        "ADV-13": _case(
            "ADV-13",
            [
                {"speaker": "Interviewer Adversarial", "text": "Você tem experiência com Azure?"},
                {"speaker": "Candidate Adversarial", "text": "Tenho cinco anos trabalhando com Azure."},
                {"speaker": "Interviewer Adversarial", "text": "Como configuraria uma managed identity?"},
                {"speaker": "Candidate Adversarial", "text": "Eu colocaria a credencial em uma variável e configuraria de algum jeito."},
            ],
        ),
        "ADV-14": _case(
            "ADV-14",
            [
                {"speaker": "Interviewer Adversarial", "text": "Você já usou Application Insights?"},
                {"speaker": "Candidate Adversarial", "text": "No meu projeto usamos Application Insights com correlation ID para rastrear a requisição entre API e serviço downstream."},
            ],
        ),
        "ADV-15": _case(
            "ADV-15",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como funciona essa configuração?"},
                {"speaker": "Candidate Adversarial", "text": "Não lembro exatamente como funciona essa configuração."},
            ],
        ),
        "ADV-16": _case(
            "ADV-16",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como investigaria uma falha de observabilidade?"},
                {"speaker": "Candidate Adversarial", "text": "Não sei exatamente, mas eu investigaria começando pelo Application Insights e verificaria dependencies."},
            ],
        ),
        "ADV-17": _case(
            "ADV-17",
            [
                {"speaker": "Interviewer Adversarial", "text": "Você já trabalhou com Kubernetes?"},
                {"speaker": "Candidate Adversarial", "text": "Sim, em produção."},
                {"speaker": "Interviewer Adversarial", "text": "Qual era sua responsabilidade no cluster?"},
                {"speaker": "Candidate Adversarial", "text": "Na verdade eu nunca administrei o cluster, só consumia deployments feitos por outra equipe."},
            ],
        ),
        "ADV-18": _case(
            "ADV-18",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como resolveria esse problema?"},
                {"speaker": "Candidate Adversarial", "text": "Eu usaria X."},
                {"speaker": "Interviewer Adversarial", "text": "Mas X não resolveria esse problema."},
                {"speaker": "Candidate Adversarial", "text": "Ah, verdade, nesse caso eu usaria Y."},
            ],
        ),
        "ADV-19": _case(
            "ADV-19",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como investigaria a falha?"},
                {"speaker": "UNKNOWN", "text": "Eu começaria pelos logs."},
            ],
        ),
        "ADV-20": _case(
            "ADV-20",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como você corrigiria o termo?"},
                {"speaker": "Candidate Adversarial", "text": "Eu procuraria o Spring Boto no contexto e preservaria o trecho original."},
            ],
            reconstructions={"R1": "Eu procuraria o Spring Boot no contexto e preservaria o trecho original."},
        ),
        "ADV-21": _case(
            "ADV-21",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como investigaria a latência?"},
                {"speaker": "Candidate Adversarial", "text": "Eu investigaria primeiro o..."},
                {"speaker": "Interviewer Adversarial", "text": "Tudo bem, pode continuar."},
                {"speaker": "Interviewer Adversarial", "text": "Qual ferramenta você usaria?"},
                {"speaker": "Candidate Adversarial", "text": "Application Insights."},
            ],
        ),
        "ADV-22": _case(
            "ADV-22",
            [{"speaker": "Interviewer Adversarial", "text": "Explique virtual threads?"}],
        ),
        "ADV-23": _case(
            "ADV-23",
            [{"speaker": "Candidate Adversarial", "text": "Nesse projeto usamos Kafka para desacoplar os serviços."}],
        ),
        "ADV-24": _case(
            "ADV-24",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como escolheria uma estratégia de retry?"},
                {"speaker": "Candidate Adversarial", "text": "Eu usaria retry com backoff, mas aplicaria retry agressivo em qualquer erro."},
            ],
        ),
        "ADV-25": _case(
            "ADV-25",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como desenharia uma API resiliente?"},
                {"speaker": "Candidate Adversarial", "text": "Eu usaria retries com backoff; não tenho certeza se aplicaria circuit breaker, mas provavelmente usaria cache e, na verdade, cache não seria adequado para dados sempre consistentes."},
            ],
        ),
        "ADV-26": _case(
            "ADV-26",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como faria troubleshooting de latência?"},
                {"speaker": "Interviewer Adversarial", "text": "Normalmente começamos pelo Application Insights."},
                {"speaker": "Candidate Adversarial", "text": "Eu começaria olhando requests e dependencies."},
            ],
        ),
        "ADV-27": _case(
            "ADV-27",
            [
                {"speaker": "Candidate Adversarial", "text": "Vocês usam Azure Monitor ou outra ferramenta?"},
                {"speaker": "Interviewer Adversarial", "text": "Usamos Azure Monitor."},
            ],
        ),
        "ADV-28": _case(
            "ADV-28",
            [
                {"speaker": "Interviewer Adversarial", "text": "Qual opção você escolheria?"},
                {"speaker": "Candidate Adversarial", "text": "Eu escolheria a opção correta porque Kafka não suporta mensagens e por isso Redis é sempre melhor."},
            ],
        ),
        "ADV-29": _case(
            "ADV-29",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como investigaria latência?"},
                {"speaker": "Candidate Adversarial", "text": "Mediria p95 e separaria dependências."},
            ],
        ),
        "ADV-30-A": _case(
            "ADV-30-A",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como investigaria latência?"},
                {"speaker": "Candidate Adversarial", "text": "Mediria p95 e separaria dependências. Sou pleno."},
            ],
        ),
        "ADV-30-B": _case(
            "ADV-30-B",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como investigaria latência?"},
                {"speaker": "Candidate Adversarial", "text": "Mediria p95 e separaria dependências. Sou sênior."},
            ],
        ),
        "ADV-BLOCKED": _case(
            "ADV-BLOCKED",
            [{"speaker": "Interviewer Adversarial", "text": "Explique virtual threads?"}],
            validation_blockers=["critical structural source failure"],
        ),
        "ADV-WARNING": _case(
            "ADV-WARNING",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como investigaria a falha?"},
                {"speaker": "UNKNOWN", "text": "Eu começaria pelos logs."},
            ],
        ),
        "ADV-LOW-RECON": _case(
            "ADV-LOW-RECON",
            [
                {"speaker": "Interviewer Adversarial", "text": "Como corrigiria o termo?"},
                {"speaker": "Candidate Adversarial", "text": "Spring Boto pode significar Spring Boot.", "reconstruction_confidence": "low"},
            ],
            reconstructions={"R1": "Spring Boto pode significar Spring Boot."},
        ),
    }


def adversarial_oracles():
    return {
        "ADV-01": {"must_have": ["contradiction"]},
        "ADV-02": {"must_have": ["self_correction", "technical_error"]},
        "ADV-03": {"must_have": ["self_correction", "technical_error"]},
        "ADV-04": {"must_have": ["confirmation"], "must_not_have": ["reasoning"]},
        "ADV-05": {"must_have": ["confirmation"], "must_not_have": ["demonstrated_experience"]},
        "ADV-06": {"response_segments": 2},
        "ADV-07": {"question_relations": ["follow_up"]},
        "ADV-08": {"question_relations": ["follow_up"], "evaluations": 2},
        "ADV-09": {"must_have": ["off_topic"]},
        "ADV-10": {"max_score": 8.0},
        "ADV-11": {"max_score": 8.0},
        "ADV-12": {"min_score": 4.0},
        "ADV-13": {"must_have": ["experience_declaration"], "must_not_have": ["demonstrated_experience"]},
        "ADV-14": {"must_have": ["demonstrated_experience"]},
        "ADV-15": {"must_have": ["uncertainty"], "must_not_have": ["technical_error"]},
        "ADV-16": {"must_have": ["uncertainty", "hypothesis"], "must_not_have": ["demonstrated_experience"]},
        "ADV-17": {"must_have": ["contradiction"]},
        "ADV-18": {"must_have": ["self_correction"]},
        "ADV-19": {"readiness": "READY_WITH_WARNINGS"},
        "ADV-20": {"preserve_original": "Spring Boto"},
        "ADV-21": {"no_invented_continuation": True},
        "ADV-22": {"missing": True},
        "ADV-23": {"unknown_question": True},
        "ADV-24": {"must_have": ["technical_error"], "partial": True},
        "ADV-25": {"must_have": ["contradiction", "uncertainty", "hypothesis"]},
        "ADV-26": {"interviewer_content_not_candidate_evidence": True},
        "ADV-27": {"candidate_question_not_evaluated": True},
        "ADV-28": {"must_have": ["technical_error"]},
        "ADV-29": {"equivalent_to": "ADV-12"},
        "ADV-30-A": {"equivalent_to": "ADV-30-B"},
        "ADV-30-B": {"equivalent_to": "ADV-30-A"},
        "ADV-BLOCKED": {"readiness": "BLOCKED"},
        "ADV-WARNING": {"readiness": "READY_WITH_WARNINGS"},
        "ADV-LOW-RECON": {"reconstruction_confidence": "low"},
    }


def blind_adversarial_input(fixture):
    forbidden = {
        "oracle",
        "expected_score",
        "expected_dimensions",
        "expected_quality",
        "adversarial_label",
        "evidence_specs",
        "evaluation_specs",
    }
    return {
        key: deepcopy(value)
        for key, value in fixture.items()
        if key not in forbidden
    }
