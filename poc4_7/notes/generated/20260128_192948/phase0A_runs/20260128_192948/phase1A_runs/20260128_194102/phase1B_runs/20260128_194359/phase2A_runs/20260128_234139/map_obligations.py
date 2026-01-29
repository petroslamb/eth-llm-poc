#!/usr/bin/env python3
"""
Map EIP-1559 obligations from Phase 1B to geth implementation.
Reads obligations_index.csv and creates client_obligations_index.csv with geth mappings.
"""

import csv
import os

# Define geth mappings for each obligation
GETH_MAPPINGS = {
    "EIP1559-OBL-001": {
        "client_locations": "[core/vm/instructions.go:419-423, core/state_transition.go:194-198, core/types/tx_dynamic_fee.go:100-109]",
        "client_code_flow": "1. Transaction converted to Message via TransactionToMessage (state_transition.go:176-203)\n2. If baseFee provided, msg.GasPrice set to effectiveGasPrice (state_transition.go:194-198)\n3. effectiveGasPrice = min(gasTipCap, gasFeeCap - baseFee) + baseFee (tx_dynamic_fee.go:100-109)\n4. EVM context created with msg.GasPrice as TxContext.GasPrice (evm.go:142-147)\n5. GASPRICE opcode (0x3a) executed via opGasprice (instructions.go:419-423)\n6. opGasprice pushes evm.GasPrice onto stack (instructions.go:420-421)\n7. evm.GasPrice equals effective_gas_price calculated in step 3"
    },
    "EIP1559-OBL-002": {
        "client_locations": "[consensus/ethash/consensus.go:276-286, core/state_processor.go:64-69, core/blockchain.go:1876-1912]",
        "client_code_flow": "1. Block validation occurs in blockchain.insertChain (blockchain.go:1876-1912)\n2. Engine.VerifyHeader checks header validity including gas_used <= gas_limit (ethash/consensus.go:276-286)\n3. state_processor.Process accumulates usedGas from all transactions (state_processor.go:60-138)\n4. GasPool initialized with block.GasLimit (state_processor.go:69)\n5. Each transaction deducts gas via gp.SubGas (state_transition.go:295)\n6. Final validation in blockchain.writeBlockWithState checks gasUsed matches header (blockchain.go:1990-1998)\n7. If gas_used > gas_limit, block rejected"
    },
    "EIP1559-OBL-003": {
        "client_locations": "[consensus/misc/gaslimit.go:27-41, consensus/misc/eip1559/eip1559.go:34-41, params/protocol_params.go:34]",
        "client_code_flow": "1. Header validation calls VerifyEIP1559Header (eip1559/eip1559.go:33-53)\n2. For London fork, parentGasLimit adjusted by ElasticityMultiplier for fork block (eip1559.go:36-38)\n3. VerifyGaslimit checks gas limit bounds (gaslimit.go:27-41)\n4. Calculates diff = |parentGasLimit - headerGasLimit| (gaslimit.go:29-32)\n5. limit = parentGasLimit / GasLimitBoundDivisor (1024) (gaslimit.go:33, params/protocol_params.go:34)\n6. If diff >= limit, returns error (gaslimit.go:34-35)\n7. Ensures headerGasLimit < parentGasLimit + parentGasLimit // 1024"
    },
    "EIP1559-OBL-004": {
        "client_locations": "[consensus/misc/gaslimit.go:27-41, consensus/misc/eip1559/eip1559.go:34-41, params/protocol_params.go:34]",
        "client_code_flow": "1. Header validation calls VerifyEIP1559Header (eip1559/eip1559.go:33-53)\n2. For London fork, parentGasLimit adjusted by ElasticityMultiplier for fork block (eip1559.go:36-38)\n3. VerifyGaslimit checks gas limit bounds (gaslimit.go:27-41)\n4. Calculates diff = |parentGasLimit - headerGasLimit| (gaslimit.go:29-32)\n5. limit = parentGasLimit / GasLimitBoundDivisor (1024) (gaslimit.go:33, params/protocol_params.go:34)\n6. If diff >= limit, returns error (gaslimit.go:34-35)\n7. Ensures headerGasLimit > parentGasLimit - parentGasLimit // 1024"
    },
    "EIP1559-OBL-005": {
        "client_locations": "[consensus/misc/gaslimit.go:37-39, params/protocol_params.go:33]",
        "client_code_flow": "1. Header validation calls VerifyGaslimit (gaslimit.go:27-41)\n2. After checking adjustment bounds, validates minimum (gaslimit.go:37-39)\n3. If headerGasLimit < params.MinGasLimit (5000), returns error (gaslimit.go:37-39)\n4. MinGasLimit constant defined at params/protocol_params.go:33\n5. This check applies to all blocks regardless of fork"
    },
    "EIP1559-OBL-006": {
        "client_locations": "[consensus/misc/eip1559/eip1559.go:46-60, params/protocol_params.go:141]",
        "client_code_flow": "1. VerifyEIP1559Header validates base fee (eip1559/eip1559.go:33-53)\n2. CalcBaseFee computes expected base fee (eip1559.go:56-98)\n3. If !config.IsLondon(parent.Number), returns InitialBaseFee (eip1559.go:58-60)\n4. InitialBaseFee = 1000000000 (1 Gwei) defined at params/protocol_params.go:141\n5. Checks header.BaseFee == expectedBaseFee (eip1559.go:48)\n6. If mismatch, returns error with details (eip1559.go:49-50)"
    },
    "EIP1559-OBL-007": {
        "client_locations": "[consensus/misc/eip1559/eip1559.go:62-66]",
        "client_code_flow": "1. CalcBaseFee calculates expected base fee (eip1559.go:56-98)\n2. parentGasTarget = parent.GasLimit / config.ElasticityMultiplier() (eip1559.go:62)\n3. ElasticityMultiplier = 2, so target is half the gas limit\n4. If parent.GasUsed == parentGasTarget (eip1559.go:64)\n5. Returns parent.BaseFee unchanged (eip1559.go:65)\n6. No adjustment when usage equals target"
    },
    "EIP1559-OBL-008": {
        "client_locations": "[consensus/misc/eip1559/eip1559.go:73-83, params/protocol_params.go:142]",
        "client_code_flow": "1. CalcBaseFee calculates new base fee (eip1559.go:56-98)\n2. If parent.GasUsed > parentGasTarget (eip1559.go:73)\n3. Calculate delta: num = parent.GasUsed - parentGasTarget (eip1559.go:76)\n4. num = num * parent.BaseFee (eip1559.go:77)\n5. num = num / parentGasTarget (eip1559.go:78)\n6. num = num / BaseFeeChangeDenominator (8) (eip1559.go:79, params:142)\n7. If num < 1, return parent.BaseFee + 1 (eip1559.go:80-81)\n8. Else return parent.BaseFee + num (eip1559.go:83)\n9. Ensures minimum increase of 1"
    },
    "EIP1559-OBL-009": {
        "client_locations": "[consensus/misc/eip1559/eip1559.go:84-97, params/protocol_params.go:142]",
        "client_code_flow": "1. CalcBaseFee calculates new base fee (eip1559.go:56-98)\n2. If parent.GasUsed < parentGasTarget (eip1559.go:84)\n3. Calculate delta: num = parentGasTarget - parent.GasUsed (eip1559.go:87)\n4. num = num * parent.BaseFee (eip1559.go:88)\n5. num = num / parentGasTarget (eip1559.go:89)\n6. num = num / BaseFeeChangeDenominator (8) (eip1559.go:90, params:142)\n7. baseFee = parent.BaseFee - num (eip1559.go:92)\n8. If baseFee < 0, set to 0 (eip1559.go:93-94)\n9. Return baseFee (eip1559.go:96)"
    },
    "EIP1559-OBL-010": {
        "client_locations": "[consensus/misc/eip1559/eip1559.go:46-52]",
        "client_code_flow": "1. VerifyEIP1559Header validates header (eip1559/eip1559.go:33-53)\n2. CalcBaseFee computes expectedBaseFee from parent (eip1559.go:47)\n3. Compares header.BaseFee with expectedBaseFee (eip1559.go:48)\n4. If header.BaseFee != expectedBaseFee, returns error (eip1559.go:48-51)\n5. Error includes actual and expected values for debugging\n6. This check applies to all post-London blocks"
    },
    "EIP1559-OBL-011": {
        "client_locations": "[core/types/transaction_signing.go:254-270, core/types/transaction_signing.go:478-503]",
        "client_code_flow": "1. Transaction sender recovered via types.Sender (transaction_signing.go:201)\n2. For EIP-1559, uses modernSigner (transaction_signing.go:186-225)\n3. modernSigner.Sender checks chainID matches (transaction_signing.go:262-264)\n4. Calls recoverPlain for signature recovery (transaction_signing.go:267-269)\n5. ValidateSignatureValues checks r,s are valid secp256k1 values (transaction_signing.go:483)\n6. Ecrecover recovers public key from signature (transaction_signing.go:493)\n7. Address derived from keccak256(pubkey)[12:] (transaction_signing.go:501)\n8. Validation occurs before transaction normalization in TransactionToMessage (state_transition.go:201)"
    },
    "EIP1559-OBL-012": {
        "client_locations": "[core/state_transition.go:266-308]",
        "client_code_flow": "1. preCheck calls buyGas to validate balance (state_transition.go:409)\n2. buyGas calculates total cost: mgval = gasLimit * gasPrice (state_transition.go:267-268)\n3. For EIP-1559, uses gasFeeCap for balance check: balanceCheck = gasLimit * gasFeeCap (state_transition.go:270-273)\n4. balanceCheck += msg.Value (state_transition.go:274)\n5. Validates state.GetBalance(from) >= balanceCheck (state_transition.go:292-293)\n6. SubBalance debits full gas + value upfront (state_transition.go:306)\n7. After execution, returnGas credits unused gas (state_transition.go:655-667)\n8. Final balance >= 0 guaranteed by validation"
    },
    "EIP1559-OBL-013": {
        "client_locations": "[core/state_transition.go:266-308]",
        "client_code_flow": "1. preCheck calls buyGas (state_transition.go:409)\n2. For EIP-1559 tx, balanceCheck = gasLimit * gasFeeCap + value (state_transition.go:270-274)\n3. Compares sender balance >= balanceCheck (state_transition.go:292-293)\n4. If insufficient, returns ErrInsufficientFunds (state_transition.go:293)\n5. This ensures sender can pay maximum possible gas cost\n6. gasFeeCap = max_fee_per_gas from transaction\n7. Validation occurs before execution in preCheck"
    },
    "EIP1559-OBL-014": {
        "client_locations": "[core/state_transition.go:341-363]",
        "client_code_flow": "1. preCheck validates EIP-1559 fee parameters (state_transition.go:310-409)\n2. If IsLondon(blockNumber), checks fee caps (state_transition.go:341-363)\n3. Validates msg.GasFeeCap >= evm.Context.BaseFee (state_transition.go:359)\n4. If gasFeeCap < baseFee, returns ErrFeeCapTooLow (state_transition.go:359-361)\n5. baseFee comes from header.BaseFee passed via BlockContext\n6. This check ensures transaction can pay at least base fee\n7. Validation occurs before buyGas"
    },
    "EIP1559-OBL-015": {
        "client_locations": "[core/state_transition.go:345-348, core/types/tx_dynamic_fee.go:32]",
        "client_code_flow": "1. preCheck validates fee cap bit length (state_transition.go:345-348)\n2. Checks msg.GasFeeCap.BitLen() <= 256 (state_transition.go:345)\n3. If > 256 bits, returns ErrFeeCapVeryHigh (state_transition.go:346-347)\n4. DynamicFeeTx.GasFeeCap is *big.Int, inherently supports arbitrary precision\n5. RLP decoding in tx_dynamic_fee.go:123-125 reads GasFeeCap as big.Int\n6. Type system ensures < 2^256 through BitLen check\n7. Validation prevents overflow in fee calculations"
    },
    "EIP1559-OBL-016": {
        "client_locations": "[core/state_transition.go:349-352, core/types/tx_dynamic_fee.go:31]",
        "client_code_flow": "1. preCheck validates tip cap bit length (state_transition.go:349-352)\n2. Checks msg.GasTipCap.BitLen() <= 256 (state_transition.go:349)\n3. If > 256 bits, returns ErrTipVeryHigh (state_transition.go:350-351)\n4. DynamicFeeTx.GasTipCap is *big.Int\n5. RLP decoding in tx_dynamic_fee.go:123-125 reads GasTipCap as big.Int\n6. Type system ensures < 2^256 through BitLen check\n7. Validation occurs in preCheck before execution"
    },
    "EIP1559-OBL-017": {
        "client_locations": "[core/state_transition.go:353-356]",
        "client_code_flow": "1. preCheck validates fee relationship (state_transition.go:353-356)\n2. Checks msg.GasFeeCap >= msg.GasTipCap (state_transition.go:353)\n3. If gasFeeCap < gasTipCap, returns ErrTipAboveFeeCap (state_transition.go:354-355)\n4. This ensures max fee can cover priority fee\n5. Validation occurs after bit length checks\n6. Prevents invalid effective gas price calculation"
    },
    "EIP1559-OBL-018": {
        "client_locations": "[core/types/tx_dynamic_fee.go:100-109, core/state_transition.go:194-198]",
        "client_code_flow": "1. TransactionToMessage converts tx to Message (state_transition.go:176-203)\n2. For EIP-1559 tx with baseFee, calculates effectiveGasPrice (state_transition.go:194-198)\n3. Calls tx.effectiveGasPrice (tx_dynamic_fee.go:100-109)\n4. tip = gasFeeCap - baseFee (tx_dynamic_fee.go:104)\n5. If tip > gasTipCap, tip = gasTipCap (tx_dynamic_fee.go:105-106)\n6. Return tip + baseFee (tx_dynamic_fee.go:108)\n7. This implements: priority_fee = min(max_priority_fee_per_gas, max_fee_per_gas - base_fee_per_gas)\n8. effectiveGasPrice set to msg.GasPrice for EVM context"
    },
    "EIP1559-OBL-019": {
        "client_locations": "[core/types/tx_dynamic_fee.go:100-109, core/state_transition.go:194-198, core/vm/instructions.go:419-423]",
        "client_code_flow": "1. TransactionToMessage calculates effectiveGasPrice (state_transition.go:194-198)\n2. tx.effectiveGasPrice computes tip + baseFee (tx_dynamic_fee.go:100-109)\n3. tip = min(gasTipCap, gasFeeCap - baseFee) (tx_dynamic_fee.go:104-106)\n4. effectiveGasPrice = tip + baseFee (tx_dynamic_fee.go:108)\n5. Set as msg.GasPrice (state_transition.go:198)\n6. EVM TxContext.GasPrice set to msg.GasPrice (evm.go:142-147)\n7. GASPRICE opcode returns evm.GasPrice (instructions.go:420)\n8. This equals priority_fee_per_gas + base_fee_per_gas"
    },
    "EIP1559-OBL-020": {
        "client_locations": "[core/state_transition.go:266-308]",
        "client_code_flow": "1. execute calls preCheck before EVM execution (state_transition.go:434)\n2. preCheck calls buyGas (state_transition.go:409)\n3. buyGas calculates mgval = gasLimit * effectiveGasPrice (state_transition.go:267-268)\n4. For EIP-1559, effectiveGasPrice already calculated in TransactionToMessage\n5. mgval += blobGas fees if applicable (state_transition.go:276-286)\n6. SubBalance debits mgval from sender (state_transition.go:306)\n7. gasRemaining = gasLimit (state_transition.go:302)\n8. This occurs before execute's EVM call (state_transition.go:422-574)"
    },
    "EIP1559-OBL-021": {
        "client_locations": "[core/state_transition.go:266-308]",
        "client_code_flow": "1. buyGas validates sender balance (state_transition.go:266-308)\n2. balanceCheck = gasLimit * gasFeeCap + value (state_transition.go:270-274)\n3. Validates GetBalance(sender) >= balanceCheck (state_transition.go:292-293)\n4. If insufficient, returns ErrInsufficientFunds (state_transition.go:293)\n5. SubBalance debits gasLimit * effectiveGasPrice (state_transition.go:306)\n6. After execution, returnGas refunds unused (state_transition.go:655-667)\n7. Final balance guaranteed >= 0 by upfront validation"
    },
    "EIP1559-OBL-022": {
        "client_locations": "[core/state_transition.go:530-545, core/state_transition.go:634-651, core/state_transition.go:655-667]",
        "client_code_flow": "1. After EVM execution, calculate gas used (state_transition.go:528)\n2. calcRefund computes refund amount capped by quotient (state_transition.go:634-651)\n3. For London+, refund = min(gasUsed/5, state.GetRefund()) (state_transition.go:640-646)\n4. gasRemaining += refund (state_transition.go:531)\n5. returnGas credits remaining * gasPrice to sender (state_transition.go:655-667)\n6. remaining = gasRemaining * msg.GasPrice (state_transition.go:656-657)\n7. AddBalance credits sender (state_transition.go:658)\n8. Refund = (gasLimit - gasUsed + refund) * effectiveGasPrice"
    },
    "EIP1559-OBL-023": {
        "client_locations": "[core/state_transition.go:547-566]",
        "client_code_flow": "1. After returnGas, calculate miner fee (state_transition.go:547-566)\n2. effectiveTip = msg.GasPrice (state_transition.go:547)\n3. If IsLondon, effectiveTip = msg.GasPrice - baseFee (state_transition.go:548-550)\n4. This extracts priority fee portion only\n5. fee = gasUsed * effectiveTip (state_transition.go:558-559)\n6. AddBalance credits coinbase with fee (state_transition.go:560)\n7. Base fee portion (gasUsed * baseFee) is NOT credited to anyone\n8. Base fee effectively burned"
    },
    "EIP1559-OBL-024": {
        "client_locations": "[core/state_transition.go:547-566]",
        "client_code_flow": "1. After execution, calculate fees (state_transition.go:547-566)\n2. effectiveTip = msg.GasPrice - baseFee for London+ (state_transition.go:548-550)\n3. Only effectiveTip * gasUsed credited to coinbase (state_transition.go:558-560)\n4. Base fee portion: gasUsed * baseFee is subtracted from sender but NOT added to any account\n5. No AddBalance call for base fee component\n6. Total supply decreases by gasUsed * baseFee\n7. Base fee burned (removed from circulation)"
    },
    "EIP1559-OBL-025": {
        "client_locations": "[core/state_processor.go:60-138, core/blockchain.go:1990-1998]",
        "client_code_flow": "1. state_processor.Process executes all transactions (state_processor.go:60-138)\n2. usedGas accumulates across all transactions (state_processor.go:64-165)\n3. Each ApplyTransactionWithEVM adds to *usedGas (state_processor.go:105-165)\n4. Final usedGas returned in ProcessResult (state_processor.go:133-138)\n5. blockchain.writeBlockWithState validates (blockchain.go:1990-1998)\n6. Checks receipts.GasUsed == header.GasUsed (blockchain.go:1991-1994)\n7. If mismatch, returns error and rejects block"
    },
    "EIP1559-OBL-026": {
        "client_locations": "[core/types/transaction.go:109-220, core/types/tx_dynamic_fee.go:119-125, core/types/tx_dynamic_fee.go:127-141]",
        "client_code_flow": "1. Transaction.EncodeRLP encodes Type 2 tx (transaction.go:109-122)\n2. For typed tx, calls encodeTyped (transaction.go:114-121, 124-128)\n3. encodeTyped writes type byte (0x02) (transaction.go:126)\n4. Calls tx.inner.encode (tx_dynamic_fee.go:119-121)\n5. inner.encode RLP encodes DynamicFeeTx struct (tx_dynamic_fee.go:120)\n6. RLP encoding order: [chainID, nonce, gasTipCap, gasFeeCap, gas, to, value, data, accessList, v, r, s]\n7. DecodeRLP reverses: reads type, dispatches to decodeTyped (transaction.go:142-176, 200-220)\n8. Signature hash via sigHash excludes v,r,s (tx_dynamic_fee.go:127-141)"
    },
    "EIP1559-OBL-027": {
        "client_locations": "[core/types/tx_dynamic_fee.go:127-141, core/types/transaction_signing.go:254-270, core/types/transaction_signing.go:478-503]",
        "client_code_flow": "1. Signature hash computed via sigHash (tx_dynamic_fee.go:127-141)\n2. prefixedRlpHash computes keccak256(0x02 || rlp([chainID, nonce, gasTipCap, gasFeeCap, gas, to, value, data, accessList])) (tx_dynamic_fee.go:128-140)\n3. Transaction signature validated via modernSigner (transaction_signing.go:254-270)\n4. Validates chainID matches (transaction_signing.go:262-264)\n5. recoverPlain performs secp256k1 recovery (transaction_signing.go:478-503)\n6. ValidateSignatureValues checks r,s in valid secp256k1 range (transaction_signing.go:483)\n7. Ecrecover recovers public key (transaction_signing.go:493)\n8. Address = keccak256(pubkey)[12:] (transaction_signing.go:501)"
    },
    "EIP1559-OBL-028": {
        "client_locations": "[core/types/receipt.go:121-152, core/types/receipt.go:91-96]",
        "client_code_flow": "1. Receipt created via MakeReceipt (state_processor.go:175-204)\n2. Receipt.Type = tx.Type() (DynamicFeeTxType = 0x02) (state_processor.go:179)\n3. Receipt.EncodeRLP encodes receipt (receipt.go:121-135)\n4. For typed receipts, calls encodeTyped (receipt.go:132-135, 137-141)\n5. encodeTyped writes type byte (0x02) (receipt.go:138)\n6. RLP encodes receiptRLP struct (receipt.go:139-140, 91-96)\n7. receiptRLP = [PostStateOrStatus (status), CumulativeGasUsed, Bloom, Logs]\n8. Format: 0x02 || rlp([status, cumulative_gas_used, logs_bloom, logs])"
    },
    "EIP1559-OBL-029": {
        "client_locations": "[core/state_transition.go:70-117]",
        "client_code_flow": "1. execute calls IntrinsicGas (state_transition.go:446)\n2. Base cost: 21000 for tx, 53000 for contract creation (state_transition.go:73-78)\n3. Data cost: count zero bytes (4 gas) and non-zero bytes (16 gas for Istanbul) (state_transition.go:79-99)\n4. Init code cost for contract creation with Shanghai (state_transition.go:101-107)\n5. Access list cost: 2400 * len(accessList) + 1900 * storageKeys (state_transition.go:109-111)\n6. Auth list cost (EIP-7702): 2600 * len(authList) (state_transition.go:113-115)\n7. Total intrinsic gas = base + data + accessList + authList\n8. Validated gasRemaining >= intrinsic (state_transition.go:450-452)"
    },
    "EIP1559-OBL-030": {
        "client_locations": "[consensus/misc/eip1559/eip1559.go:62]",
        "client_code_flow": "1. CalcBaseFee calculates base fee for block (eip1559.go:56-98)\n2. parentGasTarget = parent.GasLimit / ElasticityMultiplier (eip1559.go:62)\n3. For fork block, parent is pre-London, so parent.GasLimit is actual target\n4. Code always divides by ElasticityMultiplier (2)\n5. This creates potential issue: fork block may not use parent.GasLimit as-is\n6. EIP-1559 spec suggests parent_gas_target = parent.gas_limit for fork block\n7. Geth implementation divides uniformly, may differ from spec intent"
    },
    "EIP1559-OBL-031": {
        "client_locations": "[consensus/misc/eip1559/eip1559.go:34-41, consensus/misc/gaslimit.go:27-41]",
        "client_code_flow": "1. VerifyEIP1559Header validates fork block gas limit (eip1559.go:33-53)\n2. If !IsLondon(parent.Number), adjusts parentGasLimit (eip1559.go:36-38)\n3. parentGasLimit = parent.GasLimit * ElasticityMultiplier (eip1559.go:37)\n4. This allows fork block gas_limit up to 2x parent without violating bounds\n5. VerifyGaslimit checks adjusted parentGasLimit (eip1559.go:39, gaslimit.go:27-41)\n6. Enables smooth transition to elastic gas limit\n7. Fork block can set gas_limit = parent.gas_limit * 2 without error"
    },
    "EIP1559-OBL-032": {
        "client_locations": "[consensus/misc/eip1559/eip1559.go:62, params/config.go:412-414]",
        "client_code_flow": "1. For post-fork blocks, CalcBaseFee calculates target (eip1559.go:56-98)\n2. parentGasTarget = parent.GasLimit / config.ElasticityMultiplier() (eip1559.go:62)\n3. ElasticityMultiplier() returns 2 for London+ (params/config.go:412-414)\n4. Gas target is half the gas limit\n5. If gas_limit = 30M, gas_target = 15M\n6. Base fee adjusts based on deviation from this target\n7. This applies to all post-London blocks"
    },
    "EIP1559-OBL-033": {
        "client_locations": "[core/txpool/legacypool/list.go:484-516, core/txpool/legacypool/legacypool.go:243-276]",
        "client_code_flow": "1. Transaction pool maintains pending map by account (legacypool.go:243)\n2. priceHeap orders transactions by effective tip (list.go:484-516)\n3. priceHeap.Less compares via cmp() (list.go:492-501)\n4. cmp calculates effectiveTip = min(gasTipCap, gasFeeCap - baseFee) (list.go:504-508)\n5. Compares effectiveTip of two transactions (list.go:505)\n6. For equal tips, compares gasFeeCap, then gasTipCap (list.go:511-515)\n7. Time-based ordering for equal priority NOT explicitly implemented\n8. Mempool ordering is non-consensus implementation detail"
    },
    "EIP1559-OBL-034": {
        "client_locations": "[core/txpool/legacypool/list.go:484-516, core/miner/ordering.go:89-108]",
        "client_code_flow": "1. Block builder selects transactions via transactionsByPriceAndNonce (ordering.go:89-108)\n2. Maintains per-account sorted by nonce, global sorted by price (ordering.go:91-102)\n3. Price comparison uses effectiveTip (gasPrice - baseFee for London+) \n4. Higher effectiveTip = higher revenue for miner (ordering.go:104-105)\n5. priceHeap ensures highest paying transactions selected first (list.go:484-516)\n6. Rational miner behavior favors high priority fee transactions\n7. Not enforced by consensus, emergent from economic incentives\n8. Implementation in txpool and miner packages"
    },
}

def main():
    input_csv = "/Users/petros/Projects/eth-llm/poc4_7/notes/generated/20260128_192948/phase0A_runs/20260128_192948/phase1A_runs/20260128_194102/phase1B_runs/20260128_194359/obligations_index.csv"
    output_csv = "/Users/petros/Projects/eth-llm/poc4_7/notes/generated/20260128_192948/phase0A_runs/20260128_192948/phase1A_runs/20260128_194102/phase1B_runs/20260128_194359/phase2A_runs/20260128_234139/client_obligations_index.csv"

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Read input CSV and write output CSV
    with open(input_csv, 'r', encoding='utf-8') as infile, \
         open(output_csv, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)

        # Add new columns to fieldnames
        fieldnames = reader.fieldnames + ['client_locations', 'client_code_flow', 'client_obligation_gap', 'client_code_gap']

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each row
        for row in reader:
            obligation_id = row['id']

            # Get geth mapping if available
            if obligation_id in GETH_MAPPINGS:
                mapping = GETH_MAPPINGS[obligation_id]
                row['client_locations'] = mapping['client_locations']
                row['client_code_flow'] = mapping['client_code_flow']
            else:
                row['client_locations'] = ''
                row['client_code_flow'] = ''

            # Leave gap columns empty
            row['client_obligation_gap'] = ''
            row['client_code_gap'] = ''

            writer.writerow(row)

    print(f"✓ Successfully created {output_csv}")
    print(f"✓ Mapped {len(GETH_MAPPINGS)} obligations to geth implementation")

if __name__ == '__main__':
    main()
