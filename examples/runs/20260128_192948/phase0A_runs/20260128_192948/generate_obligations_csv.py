#!/usr/bin/env python3
"""Generate EIP-1559 obligations CSV."""

import csv

# Define obligations extracted from EIP-1559
obligations = [
    {
        "id": "EIP1559-OBL-001",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "The GASPRICE opcode (0x3a) MUST return the effective_gas_price."
    },
    {
        "id": "EIP1559-OBL-002",
        "category": "block validation",
        "enforcement_type": "consensus",
        "statement": "Block gas_used MUST be less than or equal to block gas_limit."
    },
    {
        "id": "EIP1559-OBL-003",
        "category": "block validation",
        "enforcement_type": "consensus",
        "statement": "Block gas_limit MUST be less than parent_gas_limit + parent_gas_limit // 1024."
    },
    {
        "id": "EIP1559-OBL-004",
        "category": "block validation",
        "enforcement_type": "consensus",
        "statement": "Block gas_limit MUST be greater than parent_gas_limit - parent_gas_limit // 1024."
    },
    {
        "id": "EIP1559-OBL-005",
        "category": "block validation",
        "enforcement_type": "consensus",
        "statement": "Block gas_limit MUST be at least 5000."
    },
    {
        "id": "EIP1559-OBL-006",
        "category": "base fee adjustment",
        "enforcement_type": "consensus",
        "statement": "On the fork block (INITIAL_FORK_BLOCK_NUMBER), the base_fee_per_gas MUST be set to INITIAL_BASE_FEE (1000000000)."
    },
    {
        "id": "EIP1559-OBL-007",
        "category": "base fee adjustment",
        "enforcement_type": "consensus",
        "statement": "If parent_gas_used equals parent_gas_target, then base_fee_per_gas MUST remain equal to parent_base_fee_per_gas."
    },
    {
        "id": "EIP1559-OBL-008",
        "category": "base fee adjustment",
        "enforcement_type": "consensus",
        "statement": "If parent_gas_used is greater than parent_gas_target, then base_fee_per_gas MUST increase by at least 1 and by max(parent_base_fee_per_gas * gas_used_delta // parent_gas_target // BASE_FEE_MAX_CHANGE_DENOMINATOR, 1)."
    },
    {
        "id": "EIP1559-OBL-009",
        "category": "base fee adjustment",
        "enforcement_type": "consensus",
        "statement": "If parent_gas_used is less than parent_gas_target, then base_fee_per_gas MUST decrease by parent_base_fee_per_gas * gas_used_delta // parent_gas_target // BASE_FEE_MAX_CHANGE_DENOMINATOR."
    },
    {
        "id": "EIP1559-OBL-010",
        "category": "block validation",
        "enforcement_type": "consensus",
        "statement": "The block's base_fee_per_gas MUST equal the expected_base_fee_per_gas calculated from the parent block."
    },
    {
        "id": "EIP1559-OBL-011",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "Transaction signature and chain ID MUST be validated before normalizing the transaction."
    },
    {
        "id": "EIP1559-OBL-012",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "Signer balance after deducting transaction amount MUST be greater than or equal to 0."
    },
    {
        "id": "EIP1559-OBL-013",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "Signer balance MUST be at least transaction.gas_limit * transaction.max_fee_per_gas."
    },
    {
        "id": "EIP1559-OBL-014",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "Transaction max_fee_per_gas MUST be greater than or equal to block base_fee_per_gas."
    },
    {
        "id": "EIP1559-OBL-015",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "Transaction max_fee_per_gas MUST be less than 2**256."
    },
    {
        "id": "EIP1559-OBL-016",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "Transaction max_priority_fee_per_gas MUST be less than 2**256."
    },
    {
        "id": "EIP1559-OBL-017",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "Transaction max_fee_per_gas MUST be greater than or equal to transaction max_priority_fee_per_gas."
    },
    {
        "id": "EIP1559-OBL-018",
        "category": "execution semantics",
        "enforcement_type": "consensus",
        "statement": "The priority_fee_per_gas MUST be the minimum of max_priority_fee_per_gas and (max_fee_per_gas - base_fee_per_gas)."
    },
    {
        "id": "EIP1559-OBL-019",
        "category": "execution semantics",
        "enforcement_type": "consensus",
        "statement": "The effective_gas_price MUST equal priority_fee_per_gas + base_fee_per_gas."
    },
    {
        "id": "EIP1559-OBL-020",
        "category": "execution semantics",
        "enforcement_type": "consensus",
        "statement": "Signer balance MUST be debited by transaction.gas_limit * effective_gas_price before transaction execution."
    },
    {
        "id": "EIP1559-OBL-021",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "Signer balance after deducting gas costs MUST be greater than or equal to 0."
    },
    {
        "id": "EIP1559-OBL-022",
        "category": "execution semantics",
        "enforcement_type": "consensus",
        "statement": "After transaction execution, signer MUST be refunded (gas_limit - gas_used) * effective_gas_price."
    },
    {
        "id": "EIP1559-OBL-023",
        "category": "fees",
        "enforcement_type": "consensus",
        "statement": "The miner (block author) MUST receive only the priority fee (gas_used * priority_fee_per_gas), not the base fee."
    },
    {
        "id": "EIP1559-OBL-024",
        "category": "fees",
        "enforcement_type": "consensus",
        "statement": "The base fee MUST be burned (not given to any party)."
    },
    {
        "id": "EIP1559-OBL-025",
        "category": "block validation",
        "enforcement_type": "consensus",
        "statement": "The cumulative_transaction_gas_used MUST equal the block's gas_used."
    },
    {
        "id": "EIP1559-OBL-026",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "Type 2 transactions MUST have TransactionPayload formatted as rlp([chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, destination, amount, data, access_list, signature_y_parity, signature_r, signature_s])."
    },
    {
        "id": "EIP1559-OBL-027",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "Type 2 transaction signature MUST be a secp256k1 signature over keccak256(0x02 || rlp([chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, destination, amount, data, access_list]))."
    },
    {
        "id": "EIP1559-OBL-028",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "Type 2 transaction ReceiptPayload MUST be formatted as rlp([status, cumulative_transaction_gas_used, logs_bloom, logs])."
    },
    {
        "id": "EIP1559-OBL-029",
        "category": "tx validation",
        "enforcement_type": "consensus",
        "statement": "The intrinsic cost of Type 2 transactions MUST be 21000 + 16 * non-zero calldata bytes + 4 * zero calldata bytes + 1900 * access list storage key count + 2400 * access list address count."
    },
    {
        "id": "EIP1559-OBL-030",
        "category": "block validation",
        "enforcement_type": "consensus",
        "statement": "On the fork block, parent_gas_target MUST be set to parent.gas_limit (not divided by ELASTICITY_MULTIPLIER)."
    },
    {
        "id": "EIP1559-OBL-031",
        "category": "block validation",
        "enforcement_type": "consensus",
        "statement": "On the fork block, parent_gas_limit MUST be multiplied by ELASTICITY_MULTIPLIER when validating the current block's gas_limit."
    },
    {
        "id": "EIP1559-OBL-032",
        "category": "block validation",
        "enforcement_type": "consensus",
        "statement": "After the fork block, parent_gas_target MUST be calculated as parent.gas_limit // ELASTICITY_MULTIPLIER."
    },
    {
        "id": "EIP1559-OBL-033",
        "category": "execution semantics",
        "enforcement_type": "",
        "statement": "Transactions with the same priority fee SHOULD be sorted by time received to protect against spam attacks."
    },
    {
        "id": "EIP1559-OBL-034",
        "category": "execution semantics",
        "enforcement_type": "",
        "statement": "Miners SHOULD prefer transactions with higher priority fees from a selfish mining perspective."
    }
]

# Define CSV columns
columns = [
    "id",
    "category",
    "enforcement_type",
    "statement",
    "locations",
    "code_flow",
    "obligation_gap",
    "code_gap"
]

# Write CSV file
output_path = "/Users/petros/Projects/eth-llm/poc4_7/notes/generated/20260128_192948/phase0A_runs/20260128_192948/obligations_index.csv"

with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns, quoting=csv.QUOTE_MINIMAL)

    # Write header
    writer.writeheader()

    # Write each obligation
    for obl in obligations:
        row = {
            "id": obl["id"],
            "category": obl["category"],
            "enforcement_type": obl["enforcement_type"],
            "statement": obl["statement"],
            "locations": "",
            "code_flow": "",
            "obligation_gap": "",
            "code_gap": ""
        }
        writer.writerow(row)

print(f"Successfully wrote {len(obligations)} obligations to {output_path}")
