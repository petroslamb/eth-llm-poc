# Ethereum Consensus Specs Overview

This document summarizes the structure and organization of the [ethereum/consensus-specs](https://github.com/ethereum/consensus-specs) repository.

## Architecture Overview

Unlike execution-specs which uses standalone fork directories, consensus-specs organizes specifications as **markdown documents per fork**, with each fork building upon and referencing previous forks.

### Directory Structure

```
specs/
├── phase0/          # Base beacon chain spec
├── altair/          # Light clients, sync committees
├── bellatrix/       # The Merge (PoS transition)
├── capella/         # Withdrawals
├── deneb/           # Proto-danksharding (blobs)
├── electra/         # Max balance increase, EL-triggered exits
├── fulu/            # PeerDAS, blob scheduling
├── gloas/           # Under development
└── _features/       # Standalone EIP specs not yet in a fork
    ├── eip6800/     # Verkle trees
    ├── eip6914/     # Validator index reuse
    ├── eip7441/     # Shuffling phase
    ├── eip7805/     # Inclusion lists
    ├── eip7928/     
    └── eip8025/
```

## Current Fork Status (as of 2026-01)

| Seq | Fork | Epoch | Mainnet Date | Key EIPs |
|-----|------|-------|--------------|----------|
| 0 | **Phase0** | 0 | Dec 2020 | Base beacon chain |
| 1 | **Altair** | 74240 | Oct 2021 | Sync committees, light clients |
| 2 | **Bellatrix** | 144896 | Sep 2022 | The Merge (PoS) |
| 3 | **Capella** | 194048 | Apr 2023 | Validator withdrawals |
| 4 | **Deneb** | 269568 | Mar 2024 | EIP-4844 proto-danksharding |
| 5 | **Electra** | 364032 | May 2025 | EIP-7251, EIP-6110, EIP-7002, EIP-7549, EIP-7691 |
| 6 | **Fulu** | 411392 | Dec 2025 | EIP-7594 PeerDAS, EIP-7917, EIP-7892 |
| 7 | **Gloas** | TBD | TBD | Under development |

## Finding Fork → EIP Mappings

| Location | Description |
|----------|-------------|
| [README.md](https://github.com/ethereum/consensus-specs#stable-specifications) | Fork table with epochs and links |
| `specs/<fork>/beacon-chain.md` | Introduction section lists all EIPs |
| `configs/mainnet.yaml` | Fork versions and epochs, all constants |
| `presets/mainnet/<fork>.yaml` | Fork-specific preset values |

## Key Differences from Execution Specs

| Aspect | Execution Specs | Consensus Specs |
|--------|-----------------|-----------------|
| Format | Python code per fork | Markdown with Python snippets |
| Fork structure | Standalone dirs with all files | Incremental markdown docs |
| Activation | Block number/timestamp | Beacon chain epoch |
| Feature staging | `src/ethereum/<fork>/` | `specs/_features/<eip>/` |

## Spec Documents Per Fork

Each fork typically contains:
- `beacon-chain.md` — Core state transition logic, containers, helpers
- `fork.md` — Fork transition logic
- `validator.md` — Validator duties and behavior
- `p2p-interface.md` — Networking protocol changes
- `light-client/` — Light client protocol (from Altair)
- `weak-subjectivity.md` — Checkpoint requirements

## Paired Forks with Execution Layer

| Consensus Fork | Execution Fork | Combined Name |
|---------------|----------------|---------------|
| Bellatrix | Paris | The Merge |
| Capella | Shanghai | Shapella |
| Deneb | Cancun | Dencun |
| Electra | Prague | Pectra |
| Fulu | Osaka | Fusaka |

## Configuration vs Presets

- **Configs** (`configs/`): Runtime parameters (fork epochs, network IDs)
- **Presets** (`presets/`): Compile-time parameters (committee sizes, limits)

Two preset profiles:
- `mainnet/` — Production values
- `minimal/` — Reduced values for testing

## References

- [Rendered Specification](https://ethereum.github.io/consensus-specs/)
- [Design Rationale](https://notes.ethereum.org/s/rkhCgQteN#)
- [Phase0 Onboarding](https://notes.ethereum.org/s/Bkn3zpwxB)
- [The Eth2 Book](https://eth2book.info)
- [GASPER Paper](https://arxiv.org/abs/2003.03052)
