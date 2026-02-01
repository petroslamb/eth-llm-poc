# Ethereum Execution Specs Overview

This document summarizes the structure and organization of the [ethereum/execution-specs](https://github.com/ethereum/execution-specs) repository (pyspec).

## Fork Architecture

Each fork in `src/ethereum/forks/` is a **complete, standalone implementation** that builds incrementally upon the previous fork. Each fork folder contains:

- `__init__.py` — Documents included EIPs with links
- `fork.py` — State transition function (`state_transition`)
- `blocks.py`, `transactions.py`, `state.py`, `trie.py`
- `vm/` — EVM implementation for that fork

### Key Design Principle

> "Many contributions require changes across multiple forks... ensure that differences between the forks are minimal and consist only of necessary differences."
> — [CONTRIBUTING.md](https://github.com/ethereum/execution-specs/blob/mainnet/CONTRIBUTING.md)

## Finding Fork → EIP Mappings

| Location | Description |
|----------|-------------|
| [README.md](https://github.com/ethereum/execution-specs#ethereum-protocol-releases) | Definitive table: fork names, block numbers, dates, EIPs, blog links |
| `src/ethereum/forks/<fork>/__init__.py` | Each fork's docstring lists its EIPs |
| `lists/evm/opcodes.md` | Maps opcodes to introducing fork and EIP |
| `lists/evm/proposed-opcodes.md` | Future/proposed opcodes |

## Current Fork Status (as of 2026-01)

| Fork | Status | Mainnet Date | Key EIPs |
|------|--------|--------------|----------|
| **Prague** | ✅ Live | 2025-05-07 | EIP-7702 (EOA code), EIP-2537 (BLS), EIP-7691 (blob increase) |
| **Osaka** | 🚧 Dev | 2025-12-03 | EIP-7939 (CLZ), EIP-7951 (secp256r1), EIP-7594 (PeerDAS) |
| `amsterdam`, `bpo1-5` | 🔮 Future | TBD | Placeholders |

## Branch Structure

- `mainnet` — Stable specs for all live forks
- `forks/<FORK_NAME>` — Fork under active development
- `eips/<FORK_NAME>/<EIP_NUMBER>` — Individual EIP implementation branches

## Diff Outputs

The repo generates [diff outputs](https://ethereum.github.io/execution-specs/diffs/index.html) showing changes between consecutive forks, useful for understanding incremental EIP additions.

## References

- [EIP Authors Manual](https://github.com/ethereum/execution-specs/blob/mainnet/EIP_AUTHORS_MANUAL.md) — EIP lifecycle and implementation process
- [Rendered Specification](https://ethereum.github.io/execution-specs/) — Full documentation
- [execution-spec-tests](https://github.com/ethereum/execution-spec-tests) — Test framework for generating fixtures
