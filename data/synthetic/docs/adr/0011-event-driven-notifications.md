# ADR 0011: Asynchronous Event-Driven Notifications

- **Status:** Accepted
- **Deciders:** Noah Kim, Ingrid Berg
- **Date:** 2026-06-22
- **Related Issues:** #315, #330
- **Related PRs:** #480, #505

## Context
Decoupling billing and checkout notifications from user synchronous request loop.

## Decision
Emit domain events to RabbitMQ topic exchange, consumed by [notifications/dispatcher.py](../../notifications/dispatcher.py).

## Consequences
- Sub-millisecond response latency during checkout.
