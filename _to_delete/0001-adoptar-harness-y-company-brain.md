# 0001 — Adoptar harness de ingeniería + company brain

- **Estado:** aceptada
- **Fecha:** _completar en el bootstrap_
- **Decisores:** _completar_
- **Alcance:** todos los repos de la organización

## Contexto

El desarrollo asistido por IA sin fundamentos amplifica los problemas existentes
(DORA 2025): reglas dispersas, contexto re-explicado en cada sesión, sin medición.
La organización necesita (a) una capa de gobernanza de ingeniería reutilizable y
versionada, y (b) una fuente de verdad del contexto organizacional legible por
agentes.

## Decisión

Adoptar el harness de ingeniería (template de gobernanza, consumido por releases
semver vía sync selectivo) y este company brain (repo propio de la organización)
como las dos capas de contexto que los repos importan desde sus adapters
(`CLAUDE.md` / `AGENTS.md`).

## Alternativas consideradas

- Reglas copiadas a mano en cada repo: drift inmediato, sin versionado.
- Un único repo monolítico con todo: mezcla contexto del cliente con motor
  reutilizable; imposible de actualizar sin fricción.
- Solo memoria del asistente (sin repo): no auditable, no compartible, se pierde.

## Consecuencias

- Cada repo declara en su adapter qué capas importa y en qué versión del harness está.
- El brain requiere ownership y revisión trimestral (ver `team/ownership.md`).
- La mejora del harness llega medida (lab) antes de adoptarse; el brain se refina
  con el uso.
