from copy import deepcopy


def _case(case_id, question, answer):
    return {
        "fixture_id": case_id,
        "pipeline_version": "28-reference-1",
        "participants": [
            {"participant_id": "P-CAL-CANDIDATE", "name": "Candidate Synthetic", "role": "candidate"},
            {"participant_id": "P-CAL-INTERVIEWER", "name": "Interviewer Synthetic", "role": "interviewer"},
        ],
        "raw_transcript": [
            {"id": f"{case_id}-Q", "timestamp": "11:00:00", "speaker": "Interviewer Synthetic", "text": question},
            {"id": f"{case_id}-R", "timestamp": "11:00:10", "speaker": "Candidate Synthetic", "text": answer},
        ],
    }


def calibration_fixtures():
    return {
        "CAL28-01": _case(
            "CAL28-01",
            "Como você investigaria latência em uma API?",
            "Eu mediria p95 e p99, separaria aplicação e dependências, compararia com uma janela saudável, abriria traces em produção e escolheria entre aumentar capacidade ou otimizar consultas conforme o trade-off entre custo e latência.",
        ),
        "CAL28-02": _case(
            "CAL28-02",
            "O que é injeção de dependência?",
            "É fornecer uma dependência de fora em vez de criá-la dentro da classe.",
        ),
        "CAL28-03": _case(
            "CAL28-03",
            "O que são virtual threads?",
            "São threads leves gerenciadas pela JVM para operações bloqueantes.",
        ),
        "CAL28-04": _case(
            "CAL28-04",
            "O que significa p95?",
            "É sempre o pior tempo de todas as requisições.",
        ),
        "CAL28-05": _case(
            "CAL28-05",
            "Como você lidaria com cache?",
            "Eu usaria cache para leituras frequentes, mas não detalharia invalidação nem consistência.",
        ),
        "CAL28-06": _case(
            "CAL28-06",
            "Como você decide a causa provável de um incidente?",
            "Eu compararia sintomas e métricas antes de mudar algo; se a evidência apontar para dependências, então isolaria cada uma, porque uma mudança sem hipótese pode ampliar o incidente.",
        ),
        "CAL28-07": _case(
            "CAL28-07",
            "Conte como aplicaria observabilidade em produção.",
            "Em produção configurei Application Insights, criei uma consulta KQL para dependency failures, comparei o resultado com o SLA e ajustei o timeout; o resultado foi reduzir falsos alertas.",
        ),
        "CAL28-08": _case(
            "CAL28-08",
            "Como escolheria entre cache local e distribuído?",
            "Eu escolheria cache local pela menor latência, mas cache distribuído quando a consistência entre instâncias fosse necessária; o trade-off é custo e complexidade contra coordenação.",
        ),
        "CAL28-09": _case(
            "CAL28-09",
            "Você tem experiência com Azure Monitor?",
            "Já trabalhei bastante com Azure Monitor.",
        ),
        "CAL28-10": _case(
            "CAL28-10",
            "Você tem experiência com Azure Monitor?",
            "Em produção configurei Azure Monitor, criei alertas de latência, investiguei dependency failures e documentei a decisão de reduzir o ruído sem perder sinais importantes.",
        ),
        "CAL28-11": _case(
            "CAL28-11",
            "Como funcionam virtual threads?",
            "Virtual threads são threads de plataforma; pensando melhor, não: são threads leves gerenciadas pela JVM para tarefas bloqueantes.",
        ),
        "CAL28-12": _case(
            "CAL28-12",
            "Como você desenharia uma API resiliente?",
            "Eu faria retries com backoff e provavelmente usaria circuit breaker, mas isso é uma proposta, não uma experiência que eu esteja relatando.",
        ),
        "CAL28-13": _case(
            "CAL28-13",
            "Como funciona o pipeline de observabilidade?",
            "Não lembro exatamente como funciona essa parte e não tenho certeza sobre a ordem dos componentes.",
        ),
        "CAL28-14": _case(
            "CAL28-14",
            "Como você usaria virtual threads em um serviço Java?",
            "Eu criaria uma consulta KQL para localizar dependency failures no Azure Monitor.",
        ),
        "CAL28-15": _case(
            "CAL28-15",
            "O que significa p95?",
            "É o percentil abaixo do qual está a maior parte das requisições.",
        ),
        "CAL28-16": _case(
            "CAL28-16",
            "Como você escolheria uma estratégia de retry?",
            "Eu usaria retry agressivo em qualquer erro; na verdade, retry agressivo não funcionaria em erros permanentes e pode piorar a sobrecarga.",
        ),
        "CAL28-17": _case(
            "CAL28-17",
            "Como você resolveria um incidente de latência?",
            "Em produção implementei métricas e traces, analisei a causa porque a dependência estava saturada e escolhi entre aumentar capacidade e otimizar consultas; o trade-off foi custo operacional contra latência.",
        ),
        "CAL28-18": _case(
            "CAL28-18",
            "Como investigaria latência?",
            "Mediria p95, separaria dependências e compararia com baseline.",
        ),
        "CAL28-19": _case(
            "CAL28-19",
            "Como investigaria latência?",
            "Eu começaria olhando a latência. A latência é importante porque representa tempo. Depois eu continuaria olhando a latência, talvez observando a latência e pensando que latência é o tempo de resposta.",
        ),
        "CAL28-20-A": _case(
            "CAL28-20-A",
            "Como você investigaria latência?",
            "Eu mediria p95 e separaria as dependências.",
        ),
        "CAL28-20-B": _case(
            "CAL28-20-B",
            "Como você investigaria latência?",
            "Eu mediria p95 e separaria as dependências. Sou especialista sênior com 15 anos de experiência.",
        ),
    }


def calibration_oracles():
    return {
        "CAL28-01": {"must_have": ["reasoning", "practical", "tradeoff"], "dimensions": {"correctness": "strong", "depth": "strong", "practical_application": "strong", "trade_offs": "strong"}, "score_range": (7.5, 10.0)},
        "CAL28-02": {"dimensions": {"correctness": "strong", "completeness": "partial", "depth": "weak"}, "score_range": (4.0, 8.5)},
        "CAL28-03": {"dimensions": {"correctness": "strong", "completeness": "partial"}, "score_range": (4.0, 8.5)},
        "CAL28-04": {"must_have": ["technical_error"], "dimensions": {"correctness": "weak"}, "score_range": (0.0, 5.0)},
        "CAL28-05": {"dimensions": {"correctness": "partial", "completeness": "partial"}, "score_range": (3.0, 7.5)},
        "CAL28-06": {"must_have": ["reasoning"], "dimensions": {"reasoning": "strong"}, "score_range": (5.0, 10.0)},
        "CAL28-07": {"must_have": ["demonstrated_experience", "practical"], "dimensions": {"practical_application": "strong"}, "score_range": (6.0, 10.0)},
        "CAL28-08": {"must_have": ["tradeoff"], "dimensions": {"trade_offs": "strong", "reasoning": "strong"}, "score_range": (5.0, 10.0)},
        "CAL28-09": {"must_have": ["experience_declaration"], "must_not_have": ["demonstrated_experience"], "score_range": (0.0, 6.0)},
        "CAL28-10": {"must_have": ["demonstrated_experience"], "score_range": (5.0, 10.0)},
        "CAL28-11": {"must_have": ["self_correction"], "score_range": (5.0, 10.0)},
        "CAL28-12": {"must_have": ["hypothesis"], "must_not_have": ["demonstrated_experience"], "score_range": (3.0, 8.5)},
        "CAL28-13": {"must_have": ["uncertainty"], "score_range": (0.0, 6.0)},
        "CAL28-14": {"must_have": ["off_topic"], "score_range": (0.0, 6.0)},
        "CAL28-15": {"must_have": ["na_dimension"], "score_range": (4.0, 10.0)},
        "CAL28-16": {"must_have": ["contradiction"], "score_range": (2.0, 8.0)},
        "CAL28-17": {"must_have": ["multiple_evidence_types", "demonstrated_experience", "tradeoff"], "score_range": (6.0, 10.0)},
        "CAL28-18": {"dimensions": {"correctness": "strong", "depth": "partial"}, "score_range": (5.0, 9.5)},
        "CAL28-19": {"dimensions": {"correctness": "strong", "depth": "weak"}, "score_range": (2.0, 8.0)},
        "CAL28-20-A": {"score_equivalent_to": "CAL28-20-B"},
        "CAL28-20-B": {"score_equivalent_to": "CAL28-20-A"},
    }


def blind_input(case_fixture):
    forbidden = {
        "oracle",
        "expected_score",
        "expected_score_range",
        "expected_dimensions",
        "expected_quality",
        "calibration_label",
        "evidence_specs",
        "evaluation_specs",
    }
    return {key: deepcopy(value) for key, value in case_fixture.items() if key not in forbidden}
