---
tipo: adr
titulo: "ADR-001: Remoção de GateStatus.WAIVED"
status: aceito
data: 2026-07-15
eixo: ESQ
---

# ADR-001: Remoção de GateStatus.WAIVED

## Status

Aceito

## Contexto

Durante a auditoria da FI-2A, foi identificada sobreposição semântica entre:
- `GateStatus.WAIVED` (estado terminal do processo do gate)
- `GateDecisionType.WAIVED` (resultado da decisão do gate)

Ambos tinham o string value `"waived"`, criando ambiguidade.

## Decisão

Remover `GateStatus.WAIVED` do enum. Um gate dispensado tem:
- `status = DECIDED` (o processo foi avaliado e decidido)
- `decision = WAIVED` (a decisão foi dispensar)

**Justificativa:** Não existe "processo dispensado" como conceito separado de "decisão de dispensa". Em ambos os casos, alguém TOMOU A DECISÃO de dispensar.

## Consequências

### Mais fácil
- Eliminação de ambiguidade semântica
- Máquina de estados do gate simplificada (4 estados em vez de 5)
- Código mais previsível

### Mais difícil
- Nada significativo — a distinção não tinha uso prático

## Referências

- `src/harness/domain/enums.py` — remoção de `GateStatus.WAIVED`
- `src/harness/domain/transitions.py` — remoção de `WAIVED` de `GATE_TRANSITIONS` e `GATE_TERMINAL`
- `tests/unit/domain/test_transitions.py` — novo teste `test_waived_not_in_gate_status`
