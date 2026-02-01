#!/usr/bin/env python3
"""
Generate EIP-7702 obligation locations mapping.
"""

import csv
import os

INPUT_CSV = '/home/runner/work/eth-llm-poc/eth-llm-poc/runs/ci_run/phase0A_runs/20260201_211842/obligations_index.csv'
OUTPUT_CSV = '/home/runner/work/eth-llm-poc/eth-llm-poc/runs/ci_run/phase0A_runs/20260201_211842/phase1A_runs/20260201_211953/obligations_index.csv'

# Base path prefix to strip from paths for relative location format
BASE_PATH = 'prague/'

# Mapping of obligation IDs to their code locations
OBLIGATION_LOCATIONS = {
    # OBL-001: The transaction is considered invalid if the length of authorization_list is zero.
    'EIP7702-OBL-001': '[fork.py:L510-L512, exceptions.py:L106-L109]',

    # OBL-002: A null destination is not valid for set code transactions.
    'EIP7702-OBL-002': '[fork.py:L506-L508, transactions.py:L420, exceptions.py:L32-L48]',

    # OBL-003: The transaction is invalid if auth.chain_id >= 2**256.
    # This is enforced by RLP decoding - Authorization.chain_id is U256 type
    'EIP7702-OBL-003': '[fork_types.py:L73]',

    # OBL-004: The transaction is invalid if auth.nonce >= 2**64.
    # This is enforced by RLP decoding - Authorization.nonce is U64 type
    'EIP7702-OBL-004': '[fork_types.py:L75]',

    # OBL-005: The transaction is invalid if len(auth.address) != 20.
    # This is enforced by RLP decoding - Authorization.address is Address (Bytes20)
    'EIP7702-OBL-005': '[fork_types.py:L74]',

    # OBL-006: The transaction is invalid if auth.y_parity >= 2**8.
    # This is enforced by RLP decoding - Authorization.y_parity is U8 type
    'EIP7702-OBL-006': '[fork_types.py:L76]',

    # OBL-007: The transaction is invalid if auth.r >= 2**256.
    # This is enforced by RLP decoding - Authorization.r is U256 type
    'EIP7702-OBL-007': '[fork_types.py:L77]',

    # OBL-008: The transaction is invalid if auth.s >= 2**256.
    # This is enforced by RLP decoding - Authorization.s is U256 type
    'EIP7702-OBL-008': '[fork_types.py:L78]',

    # OBL-009: The authorization list must be processed before the execution portion of the transaction begins.
    'EIP7702-OBL-009': '[vm/interpreter.py:L126-L127]',

    # OBL-010: The authorization list must be processed after the sender's nonce is incremented.
    'EIP7702-OBL-010': '[fork.py:L879, vm/interpreter.py:L126-L127]',

    # OBL-011: For each authorization tuple, the chain ID must be verified to be 0 or the ID of the current chain.
    'EIP7702-OBL-011': '[vm/eoa_delegation.py:L172-L173]',

    # OBL-012: For each authorization tuple, the nonce must be verified to be less than 2**64 - 1.
    'EIP7702-OBL-012': '[vm/eoa_delegation.py:L175-L176]',

    # OBL-013: The signature value s must be less than or equal to secp256k1n/2, as specified in EIP-2.
    'EIP7702-OBL-013': '[vm/eoa_delegation.py:L99-L100]',

    # OBL-014: The authority address recovered from ecrecover must be added to accessed_addresses as defined in EIP-2929.
    'EIP7702-OBL-014': '[vm/eoa_delegation.py:L183]',

    # OBL-015: The code of authority must be verified to be empty or already delegated.
    'EIP7702-OBL-015': '[vm/eoa_delegation.py:L185-L189]',

    # OBL-016: The nonce of authority must be verified to be equal to the nonce in the authorization tuple.
    'EIP7702-OBL-016': '[vm/eoa_delegation.py:L191-L193]',

    # OBL-017: If authority is not empty, PER_EMPTY_ACCOUNT_COST - PER_AUTH_BASE_COST gas must be added to the global refund counter.
    'EIP7702-OBL-017': '[vm/eoa_delegation.py:L195-L196, vm/eoa_delegation.py:L25-L26]',

    # OBL-018: The code of authority must be set to 0xef0100 || address (the delegation indicator).
    'EIP7702-OBL-018': '[vm/eoa_delegation.py:L200-L202, vm/eoa_delegation.py:L22-L23]',

    # OBL-019: If address is 0x0, the delegation indicator must not be written and the account's code hash must be reset to the empty code hash.
    'EIP7702-OBL-019': '[vm/eoa_delegation.py:L198-L202, vm/eoa_delegation.py:L27]',

    # OBL-020: The nonce of authority must be increased by one after processing each authorization tuple.
    'EIP7702-OBL-020': '[vm/eoa_delegation.py:L204]',

    # OBL-021: If any step in authorization processing fails, processing of that tuple must stop immediately and continue to the next tuple.
    'EIP7702-OBL-021': '[vm/eoa_delegation.py:L172-L193]',

    # OBL-022: When multiple tuples from the same authority are present, the code must be set using the address in the last valid occurrence.
    'EIP7702-OBL-022': '[vm/eoa_delegation.py:L171]',

    # OBL-023: Processed delegation indicators must not be rolled back if transaction execution results in failure.
    'EIP7702-OBL-023': '[vm/interpreter.py:L126-L127, state.py:L124-L143]',

    # OBL-024: CALL instructions targeting an address with a delegation indicator must load and execute the code at the delegated address.
    'EIP7702-OBL-024': '[vm/instructions/system.py:L382-L389, vm/eoa_delegation.py:L117-L149]',

    # OBL-025: CALLCODE instructions targeting an address with a delegation indicator must load and execute the code at the delegated address.
    'EIP7702-OBL-025': '[vm/instructions/system.py:L471-L477, vm/eoa_delegation.py:L117-L149]',

    # OBL-026: DELEGATECALL instructions targeting an address with a delegation indicator must load and execute the code at the delegated address.
    'EIP7702-OBL-026': '[vm/instructions/system.py:L612-L618, vm/eoa_delegation.py:L117-L149]',

    # OBL-027: STATICCALL instructions targeting an address with a delegation indicator must load and execute the code at the delegated address.
    'EIP7702-OBL-027': '[vm/instructions/system.py:L682-L688, vm/eoa_delegation.py:L117-L149]',

    # OBL-028: Any transaction where destination points to an address with a delegation indicator must execute the delegated code.
    'EIP7702-OBL-028': '[vm/interpreter.py:L129-L134, vm/eoa_delegation.py:L54-L71]',

    # OBL-029: CODESIZE must operate on the executing (delegated) code, not the delegation indicator.
    'EIP7702-OBL-029': '[vm/instructions/environment.py:L249-L269, vm/interpreter.py:L281]',

    # OBL-030: CODECOPY must operate on the executing (delegated) code, not the delegation indicator.
    'EIP7702-OBL-030': '[vm/instructions/environment.py:L272-L304, vm/interpreter.py:L281]',

    # OBL-031: When a precompile address is the target of a delegation, the retrieved code must be considered empty.
    'EIP7702-OBL-031': '[vm/interpreter.py:L296-L298, vm/eoa_delegation.py:L147]',

    # OBL-032: CALL, CALLCODE, STATICCALL, DELEGATECALL instructions targeting an account delegated to a precompile must execute empty code.
    'EIP7702-OBL-032': '[vm/instructions/system.py:L382-L389, vm/instructions/system.py:L471-L477, vm/instructions/system.py:L612-L618, vm/instructions/system.py:L682-L688, vm/eoa_delegation.py:L138-L139]',

    # OBL-033: In case a delegation indicator points to another delegation, clients must retrieve only the first code and stop following the delegation chain.
    'EIP7702-OBL-033': '[vm/eoa_delegation.py:L137-L149]',

    # OBL-034: The intrinsic cost of the set code transaction must include 21000 + 16 * non-zero calldata bytes + 4 * zero calldata bytes + 1900 * access list storage key count + 2400 * access list address count.
    'EIP7702-OBL-034': '[transactions.py:L564-L639, transactions.py:L26-L61]',

    # OBL-035: The intrinsic cost must additionally include PER_EMPTY_ACCOUNT_COST * authorization list length.
    'EIP7702-OBL-035': '[transactions.py:L626-L628, vm/eoa_delegation.py:L25]',

    # OBL-036: The transaction sender must pay for all authorization tuples, regardless of validity or duplication.
    'EIP7702-OBL-036': '[transactions.py:L627-L628]',

    # OBL-037: If a code executing instruction accesses a cold account during resolution of delegated code, an additional COLD_ACCOUNT_READ_COST of 2600 gas must be charged.
    'EIP7702-OBL-037': '[vm/eoa_delegation.py:L142-L146, vm/gas.py:L65]',

    # OBL-038: If a code executing instruction accesses a cold account during resolution of delegated code, the account must be added to accessed_addresses.
    'EIP7702-OBL-038': '[vm/eoa_delegation.py:L145]',

    # OBL-039: If a code executing instruction accesses a warm account during resolution of delegated code, a WARM_STORAGE_READ_COST of 100 gas must be charged.
    'EIP7702-OBL-039': '[vm/eoa_delegation.py:L142-L143, vm/gas.py:L66]',

    # OBL-040: EOAs whose code is a valid delegation indicator (0xef0100 || address) are allowed to originate transactions.
    'EIP7702-OBL-040': '[fork.py:L521-L522, vm/eoa_delegation.py:L30-L51]',

    # OBL-041: Accounts with any code value other than a valid delegation indicator may not originate transactions.
    'EIP7702-OBL-041': '[fork.py:L521-L522, vm/eoa_delegation.py:L30-L51]',

    # OBL-042: If a transaction's destination has a delegation indicator, the target of the delegation must be added to accessed_addresses.
    'EIP7702-OBL-042': '[vm/interpreter.py:L132]',

    # OBL-043: SET_CODE_TX_TYPE must be 0x04.
    'EIP7702-OBL-043': '[transactions.py:L493-L494, transactions.py:L514-L515]',

    # OBL-044: MAGIC must be 0x05.
    'EIP7702-OBL-044': '[vm/eoa_delegation.py:L21]',

    # OBL-045: PER_AUTH_BASE_COST must be 12500.
    'EIP7702-OBL-045': '[vm/eoa_delegation.py:L26]',

    # OBL-046: PER_EMPTY_ACCOUNT_COST must be 25000.
    'EIP7702-OBL-046': '[vm/eoa_delegation.py:L25]',

    # OBL-047: The transaction signature (signature_y_parity, signature_r, signature_s) must be a secp256k1 signature over keccak256(SET_CODE_TX_TYPE || TransactionPayload).
    'EIP7702-OBL-047': '[transactions.py:L696-L701, transactions.py:L838-L863]',

    # OBL-048: The authority address must be recovered using ecrecover(keccak(MAGIC || rlp([chain_id, address, nonce])), y_parity, r, s).
    'EIP7702-OBL-048': '[vm/eoa_delegation.py:L74-L114]',
}

def main():
    # Read input CSV
    with open(INPUT_CSV, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # Update locations for each row
    for row in rows:
        obligation_id = row.get('id', '')
        if obligation_id in OBLIGATION_LOCATIONS:
            row['locations'] = OBLIGATION_LOCATIONS[obligation_id]

    # Write output CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")

    # Verify the output
    with open(OUTPUT_CSV, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        output_rows = list(reader)

    print(f"Verified {len(output_rows)} rows in output file")

    if len(rows) == len(output_rows):
        print("Row count matches!")
    else:
        print(f"ERROR: Row count mismatch! Input: {len(rows)}, Output: {len(output_rows)}")

if __name__ == '__main__':
    main()
