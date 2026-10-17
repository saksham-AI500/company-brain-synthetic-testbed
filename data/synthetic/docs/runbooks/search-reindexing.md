# Runbook: Elasticsearch & Shard Reindexing

- **Service:** Search Indexer
- **Severity:** Sev-2
- **Related Issues:** #202, #305
- **Related PRs:** #415, #510

## Overview
Rebuilding search inverted index from Postgres WAL logical replication stream.
Trigger pipeline crawl in [search/indexer/pipeline.py](../../search/indexer/pipeline.py).
