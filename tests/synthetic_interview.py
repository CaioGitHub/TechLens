from copy import deepcopy


def synthetic_interview_fixture():
    participants = [
        {
            "participant_id": "P-CANDIDATE-27",
            "name": "Ana Martins",
            "role": "candidate",
            "confidence": "high",
        },
        {
            "participant_id": "P-INTERVIEWER-27",
            "name": "Bruno Lima",
            "role": "interviewer",
            "confidence": "high",
        },
        {
            "participant_id": "P-OBSERVER-27",
            "name": "Carla Souza",
            "role": "observer",
            "confidence": "high",
        },
    ]
    raw_transcript = [
        {"id": "RAW-01", "timestamp": "10:00:00", "speaker": "Bruno Lima", "text": "Como você investigaria latência em uma API?"},
        {"id": "RAW-02", "timestamp": "10:00:12", "speaker": "Ana Martins", "text": "Eu começaria por p95 e p99, separaria aplicação das dependências e compararia com uma janela saudável."},
        {"id": "RAW-03", "timestamp": "10:00:24", "speaker": "Ana Martins", "text": "Depois olharia traces para localizar onde o tempo está concentrado."},
        {"id": "RAW-04", "timestamp": "10:01:10", "speaker": "Bruno Lima", "text": "E se o banco fosse o principal suspeito?"},
        {"id": "RAW-05", "timestamp": "10:01:22", "speaker": "Ana Martins", "text": "Eu verificaria queries lentas e planos de execução..."},
        {"id": "RAW-06", "timestamp": "10:01:31", "speaker": "Bruno Lima", "text": "Pode continuar, sem problema."},
        {"id": "RAW-07", "timestamp": "10:01:42", "speaker": "Ana Martins", "text": "Também verificaria saturação de conexões antes de alterar índices."},
        {"id": "RAW-08", "timestamp": "10:02:30", "speaker": "Bruno Lima", "text": "O que significa p95?"},
        {"id": "RAW-09", "timestamp": "10:02:40", "speaker": "Ana Martins", "text": "É o maior valor observado em noventa e cinco por cento das requisições, então sempre representa o pior caso."},
        {"id": "RAW-10", "timestamp": "10:03:20", "speaker": "Bruno Lima", "text": "Como você explicaria isso para alguém do time?"},
        {"id": "RAW-11", "timestamp": "10:03:35", "speaker": "Carla Souza", "text": "A pergunta ficou sem resposta até aqui."},
        {"id": "RAW-12", "timestamp": "10:04:00", "speaker": "Bruno Lima", "text": "Reformulando: como você usaria percentis para priorizar um incidente?"},
        {"id": "RAW-13", "timestamp": "10:04:15", "speaker": "Ana Martins", "text": "Eu usaria a média. Pensando melhor, usaria p95 e p99 porque a cauda importa."},
        {"id": "RAW-14", "timestamp": "10:05:00", "speaker": "Bruno Lima", "text": "No Java 21, o que são virtual threads?"},
        {"id": "RAW-15", "timestamp": "10:05:12", "speaker": "Ana Martins", "text": "Virtual threads são threads de plataforma... espera, não. São threads leves gerenciadas pela JVM, úteis para operações bloqueantes."},
        {"id": "RAW-16", "timestamp": "10:06:00", "speaker": "Bruno Lima", "text": "Você já trabalhou com Application Insights?"},
        {"id": "RAW-17", "timestamp": "10:06:15", "speaker": "Ana Martins", "text": "Já trabalhei bastante com Application Insights."},
        {"id": "RAW-18", "timestamp": "10:06:45", "speaker": "Bruno Lima", "text": "Conte uma situação concreta em que usou observabilidade."},
        {"id": "RAW-19", "timestamp": "10:07:00", "speaker": "Ana Martins", "text": "Em produção configurei Application Insights, acompanhei dependency failures e criei uma consulta KQL para identificar aumento de latência; depois ajustamos o timeout com um trade-off de custo."},
        {"id": "RAW-20", "timestamp": "10:08:00", "speaker": "Bruno Lima", "text": "Como você desenharia uma API em arquitetura hexagonal?"},
        {"id": "RAW-21", "timestamp": "10:08:15", "speaker": "Ana Martins", "text": "Provavelmente separaria portas e adaptadores, mas validaria primeiro as restrições do domínio."},
        {"id": "RAW-22", "timestamp": "10:09:00", "speaker": "Bruno Lima", "text": "O que você faria se não encontrasse a causa de um erro 500?"},
        {"id": "RAW-23", "timestamp": "10:09:15", "speaker": "Ana Martins", "text": "Não lembro exatamente como funciona essa parte do pipeline."},
        {"id": "RAW-24", "timestamp": "10:10:00", "speaker": "Ana Martins", "text": "Posso perguntar como vocês monitoram custos?"},
        {"id": "RAW-25", "timestamp": "10:10:15", "speaker": "Bruno Lima", "text": "Depois falamos disso. Como você investigaria uma falha intermitente?"},
        {"id": "RAW-26", "timestamp": "10:10:30", "speaker": "UNKNOWN", "text": "Sim, eu acho que..."},
        {"id": "RAW-27", "timestamp": "10:11:00", "speaker": "Bruno Lima", "text": "Como você corrigiria um erro de transcrição técnica em um registro?"},
        {"id": "RAW-28", "timestamp": "10:11:15", "speaker": "Ana Martins", "text": "Eu procuraria o Spring Boto no contexto e preservaria o trecho original."},
    ]
    return {
        "fixture_id": "SYN-STAGE27-01",
        "pipeline_version": "27-reference-1",
        "participants": participants,
        "raw_transcript": raw_transcript,
        "reconstructions": {
            "R12": "Eu procuraria o Spring Boot no contexto e preservaria o trecho original."
        },
        "evidence_specs": {
            "R1": {"evidence_id": "S27-E1", "type": "reasoning", "qualification": "positive"},
            "R5": {"evidence_id": "S27-E5", "type": "technical_error", "qualification": "negative"},
            "R6": {"evidence_id": "S27-E6", "type": "self_correction", "qualification": "contradictory"},
            "R8": {"evidence_id": "S27-E8", "type": "experience_declaration", "qualification": "insufficient"},
            "R9": {"evidence_id": "S27-E9", "type": "demonstrated_experience", "qualification": "positive"},
            "R10": {"evidence_id": "S27-E10", "type": "hypothesis", "qualification": "conditional"},
            "R11": {"evidence_id": "S27-E11", "type": "uncertainty", "qualification": "insufficient"},
        },
        "evaluation_specs": {
            "Q1": {"id": "S27-EVAL-1", "score": 8.5, "confidence": "high"},
            "Q2": {"id": "S27-EVAL-2", "score": 8.0, "confidence": "high"},
            "Q3": {"id": "S27-EVAL-3", "score": 4.0, "confidence": "high"},
            "Q5": {"id": "S27-EVAL-5", "score": 7.0, "confidence": "medium"},
            "Q6": {"id": "S27-EVAL-6", "score": 8.0, "confidence": "high"},
            "Q7": {"id": "S27-EVAL-7", "score": 5.0, "confidence": "medium"},
            "Q8": {"id": "S27-EVAL-8", "score": 8.5, "confidence": "high"},
            "Q9": {"id": "S27-EVAL-9", "score": 6.0, "confidence": "medium"},
            "Q10": {"id": "S27-EVAL-10", "score": 3.0, "confidence": "low"},
            "Q12": {"id": "S27-EVAL-12", "score": 7.0, "confidence": "high"},
        },
        "oracle": {
            "must_preserve_original_transcript": True,
            "must_have_candidate_question": True,
            "must_have_missing_response": True,
            "must_have_ambiguous_segment": True,
            "must_have_experience_declaration": "R8",
            "must_have_demonstrated_experience": "R9",
            "must_have_self_correction": "R6",
            "must_have_hypothesis": "R10",
            "must_have_uncertainty": "R11",
            "must_normalize_transcription_error": "R12",
        },
    }


def clone_with_raw_text_change():
    fixture = deepcopy(synthetic_interview_fixture())
    fixture["raw_transcript"][1]["text"] += " Texto de preenchimento sem informação técnica nova."
    return fixture
