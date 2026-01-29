#!/usr/bin/env python3
"""
Map EIP-1559 obligations to implementation locations in the London fork.
"""

import csv

# Define the mappings for each obligation
obligation_mappings = {
    "EIP1559-OBL-001": [
        "vm/instructions/environment.py:304-324",  # gasprice function returns effective_gas_price
        "fork.py:789"  # where gas_price is set to effective_gas_price in tx_env
    ],
    "EIP1559-OBL-002": [
        "fork.py:320-321",  # validate_header checks gas_used <= gas_limit
        "fork.py:202-205"   # state_transition validates block_gas_used == header.gas_used
    ],
    "EIP1559-OBL-003": [
        "fork.py:884-886",  # check_gas_limit: gas_limit >= parent + delta
    ],
    "EIP1559-OBL-004": [
        "fork.py:887-888",  # check_gas_limit: gas_limit <= parent - delta
    ],
    "EIP1559-OBL-005": [
        "fork.py:889-890",  # check_gas_limit: gas_limit >= GAS_LIMIT_MINIMUM (5000)
        "fork.py:71"        # GAS_LIMIT_MINIMUM constant definition
    ],
    "EIP1559-OBL-006": [
        "fork.py:325-327",  # validate_header sets INITIAL_BASE_FEE on fork block
        "fork.py:73"        # INITIAL_BASE_FEE = 1000000000
    ],
    "EIP1559-OBL-007": [
        "fork.py:252-253",  # calculate_base_fee_per_gas: if parent_gas_used == parent_gas_target
    ],
    "EIP1559-OBL-008": [
        "fork.py:254-267",  # calculate_base_fee_per_gas: parent_gas_used > parent_gas_target, with max(..., 1)
    ],
    "EIP1559-OBL-009": [
        "fork.py:268-280",  # calculate_base_fee_per_gas: parent_gas_used < parent_gas_target
    ],
    "EIP1559-OBL-010": [
        "fork.py:329-337",  # validate_header: checks expected_base_fee_per_gas == header.base_fee_per_gas
    ],
    "EIP1559-OBL-011": [
        "fork.py:484",      # check_transaction calls recover_sender which validates signature
        "transactions.py:405-454"  # recover_sender validates signature and chain_id
    ],
    "EIP1559-OBL-012": [
        "fork.py:513-514",  # check_transaction: sender_account.balance >= max_gas_fee + tx.value
    ],
    "EIP1559-OBL-013": [
        "fork.py:502-507",  # check_transaction: max_gas_fee = tx.gas * tx.max_fee_per_gas
        "fork.py:513-514"   # validates sender_account.balance >= max_gas_fee + tx.value
    ],
    "EIP1559-OBL-014": [
        "fork.py:492-495",  # check_transaction: tx.max_fee_per_gas >= base_fee_per_gas
    ],
    "EIP1559-OBL-015": [
        "transactions.py:230-239",  # FeeMarketTransaction.max_fee_per_gas is Uint type
    ],
    "EIP1559-OBL-016": [
        "transactions.py:230-239",  # FeeMarketTransaction.max_priority_fee_per_gas is Uint type
    ],
    "EIP1559-OBL-017": [
        "fork.py:488-491",  # check_transaction: tx.max_fee_per_gas >= tx.max_priority_fee_per_gas
    ],
    "EIP1559-OBL-018": [
        "fork.py:497-500",  # check_transaction: priority_fee_per_gas = min(max_priority, max_fee - base_fee)
    ],
    "EIP1559-OBL-019": [
        "fork.py:501",      # check_transaction: effective_gas_price = priority_fee + base_fee
        "fork.py:789"       # process_transaction: tx_env.gas_price = effective_gas_price
    ],
    "EIP1559-OBL-020": [
        "fork.py:767",      # process_transaction: effective_gas_fee = tx.gas * effective_gas_price
        "fork.py:772-777"   # sender balance debited by effective_gas_fee before execution
    ],
    "EIP1559-OBL-021": [
        "fork.py:513-514",  # check_transaction validates sender balance after deduction
    ],
    "EIP1559-OBL-022": [
        "fork.py:801-817",  # process_transaction: refund calculation and credit to sender
    ],
    "EIP1559-OBL-023": [
        "fork.py:810-811",  # transaction_fee = tx_gas_used_after_refund * priority_fee_per_gas
        "fork.py:819-828"   # coinbase receives transaction_fee (only priority fee, not base fee)
    ],
    "EIP1559-OBL-024": [
        "fork.py:810-811",  # base fee is not included in transaction_fee sent to miner
        "fork.py:819-828"   # only priority_fee_per_gas goes to coinbase (base fee implicitly burned)
    ],
    "EIP1559-OBL-025": [
        "fork.py:837",      # block_output.block_gas_used accumulates tx gas used
        "fork.py:202-205"   # state_transition validates cumulative == block.header.gas_used
    ],
    "EIP1559-OBL-026": [
        "transactions.py:208-283",  # FeeMarketTransaction dataclass with all required fields
        "transactions.py:303-304"   # encode_transaction: Type 2 with b"\x02" + rlp.encode(tx)
    ],
    "EIP1559-OBL-027": [
        "transactions.py:447-452",  # recover_sender for FeeMarketTransaction
        "transactions.py:533-557"   # signing_hash_1559: keccak256(0x02 || rlp([...]))
    ],
    "EIP1559-OBL-028": [
        "blocks.py:262-292",        # Receipt dataclass structure
        "blocks.py:294-308"         # encode_receipt for FeeMarketTransaction with b"\x02" + rlp
    ],
    "EIP1559-OBL-029": [
        "transactions.py:359-402",  # calculate_intrinsic_cost with all components
        "transactions.py:26-55"     # Constants: TX_BASE_COST=21000, costs for data/access_list
    ],
    "EIP1559-OBL-030": [
        "fork.py:248",  # calculate_base_fee_per_gas: parent_gas_target = parent_gas_limit // ELASTICITY_MULTIPLIER
        # Note: On fork block, parent doesn't have base_fee, so special handling in validate_header
    ],
    "EIP1559-OBL-031": [
        "fork.py:249-250",  # calculate_base_fee_per_gas calls check_gas_limit with parent_gas_limit
        # Note: Fork block validation uses parent gas limit for validation
    ],
    "EIP1559-OBL-032": [
        "fork.py:248",  # calculate_base_fee_per_gas: parent_gas_target = parent_gas_limit // ELASTICITY_MULTIPLIER
        "fork.py:69"    # ELASTICITY_MULTIPLIER = 2
    ],
    "EIP1559-OBL-033": [
        # This is a SHOULD requirement for transaction ordering, not enforced in consensus code
    ],
    "EIP1559-OBL-034": [
        # This is a SHOULD requirement for miner behavior, not enforced in consensus code
    ],
}

def update_csv_with_mappings(input_path, output_path):
    """Read CSV, update locations column, and write to output."""

    # Read the CSV
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # Update each row with mappings
    for row in rows:
        obligation_id = row['id']
        if obligation_id in obligation_mappings:
            locations = obligation_mappings[obligation_id]
            # Format as bracketed list
            row['locations'] = '[' + ', '.join(locations) + ']'
        else:
            # Keep empty if no mapping
            row['locations'] = ''

    # Write the updated CSV
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated CSV written to: {output_path}")
    print(f"Total obligations processed: {len(rows)}")
    print(f"Obligations mapped: {len([r for r in rows if r['locations']])}")

if __name__ == '__main__':
    input_csv = '/Users/petros/Projects/eth-llm/poc4_7/notes/generated/20260128_192948/phase0A_runs/20260128_192948/obligations_index.csv'
    output_csv = '/Users/petros/Projects/eth-llm/poc4_7/notes/generated/20260128_192948/phase0A_runs/20260128_192948/phase1A_runs/20260128_194102/obligations_index.csv'

    update_csv_with_mappings(input_csv, output_csv)
