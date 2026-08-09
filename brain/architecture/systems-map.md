# Systems map

> The organization's systems/repos and how they relate. An agent working in one
> repo uses this map to know what sits upstream and downstream of its change.

## Diagram

```mermaid
graph TB
    subgraph Products
        A[_system A_]
    end
    subgraph Platform
        B[_system B_]
    end
    A --> B
```

## Inventory

| System | Repo | What it does | Stack | Owner | Criticality |
|---|---|---|---|---|---|
| _PENDING_ | | | | | |
