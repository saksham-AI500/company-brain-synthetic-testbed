# ADR 0002: Service Communication Protocols

- **Status:** Accepted
- **Deciders:** Devon Reed, Marcus Vance, Ananya Rao
- **Date:** 2025-10-12
- **Related Issues:** #18, #22
- **Related PRs:** #28, #35

## Context
High volume inter-service RPC communication between [api/gateway](../../api/gateway/router.py) and backend modules.

## Decision
We use HTTP/2 with JSON payloads for external client ingress, and gRPC with Protobuf for high-throughput internal microservice calls.

## Consequences
- High performance RPC communication.
- Rate limiting handled at ingress gateway per #215.
