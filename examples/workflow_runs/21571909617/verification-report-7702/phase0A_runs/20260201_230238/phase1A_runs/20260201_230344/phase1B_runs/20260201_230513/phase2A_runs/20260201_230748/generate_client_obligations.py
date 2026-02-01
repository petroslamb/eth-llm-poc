#!/usr/bin/env python3
"""
Generate client_obligations_index.csv from obligations_index.csv.
Maps EIP-7702 spec obligations to geth implementation locations and code flows.
"""

import csv
import os

INPUT_CSV = "/home/runner/work/eth-llm-poc/eth-llm-poc/runs/ci_run/phase0A_runs/20260201_230238/phase1A_runs/20260201_230344/phase1B_runs/20260201_230513/obligations_index.csv"
OUTPUT_CSV = "/home/runner/work/eth-llm-poc/eth-llm-poc/runs/ci_run/phase0A_runs/20260201_230238/phase1A_runs/20260201_230344/phase1B_runs/20260201_230513/phase2A_runs/20260201_230748/client_obligations_index.csv"

# Mapping of obligation ID to geth implementation locations and code flow
GETH_MAPPINGS = {
    "EIP7702-OBL-001": {
        "client_locations": "[core/types/transaction.go:L52, core/types/tx_setcode.go:L186]",
        "client_code_flow": "Transaction decoding -> transaction.go:decodeTyped() [L206-214: switch b[0] case SetCodeTxType=0x04 creates SetCodeTx]; tx_setcode.go:txType() [L186: returns SetCodeTxType]"
    },
    "EIP7702-OBL-002": {
        "client_locations": "[core/types/tx_setcode.go:L51-L67, core/types/tx_setcode.go:L220-L243]",
        "client_code_flow": "core/types/tx_setcode.go:SetCodeTx struct [L51-67: defines ChainID, Nonce, GasTipCap, GasFeeCap, Gas, To, Value, Data, AccessList, AuthList, V, R, S]; sigHash() [L228-243: computes keccak256(SetCodeTxType || rlp(fields))]"
    },
    "EIP7702-OBL-003": {
        "client_locations": "[core/types/tx_setcode.go:L57, core/types/tx_setcode.go:L196, core/state_transition.go:L402-L404]",
        "client_code_flow": "core/types/tx_setcode.go:SetCodeTx.To [L57: To common.Address - not a pointer, non-null by type]; to() [L196: returns &tmp]; core/state_transition.go:preCheck() [L402-404: if SetCodeAuthorizations != nil && msg.To == nil returns ErrSetCodeTxCreate]"
    },
    "EIP7702-OBL-004": {
        "client_locations": "[core/types/tx_setcode.go:L228-L243, core/types/transaction_signing.go:L246-L269]",
        "client_code_flow": "Transaction validation -> types.Sender() -> modernSigner.Sender() [L254-269: calls Hash(tx), ecrecover]; tx_setcode.go:sigHash() [L228-243: computes keccak256(0x04 || rlp(...))]"
    },
    "EIP7702-OBL-005": {
        "client_locations": "[core/state_transition.go:L405-L407, core/error.go:L130, core/txpool/validation.go:L149-L153]",
        "client_code_flow": "core/state_transition.go:preCheck() [L405-407: if len(SetCodeAuthorizations) == 0 returns ErrEmptyAuthList]; core/error.go [L130: ErrEmptyAuthList definition]; txpool/validation.go [L149-153: SetCodeTxType requires non-empty auth list]"
    },
    "EIP7702-OBL-006": {
        "client_locations": "[core/types/tx_setcode.go:L73]",
        "client_code_flow": "RLP decode -> SetCodeAuthorization struct [L73: ChainID uint256.Int] - uint256.Int enforces < 2^256"
    },
    "EIP7702-OBL-007": {
        "client_locations": "[core/types/tx_setcode.go:L75]",
        "client_code_flow": "RLP decode -> SetCodeAuthorization struct [L75: Nonce uint64] - uint64 type enforces < 2^64"
    },
    "EIP7702-OBL-008": {
        "client_locations": "[core/types/tx_setcode.go:L74]",
        "client_code_flow": "RLP decode -> SetCodeAuthorization struct [L74: Address common.Address] - common.Address is [20]byte, exactly 20 bytes"
    },
    "EIP7702-OBL-009": {
        "client_locations": "[core/types/tx_setcode.go:L76]",
        "client_code_flow": "RLP decode -> SetCodeAuthorization struct [L76: V uint8] - uint8 type enforces < 2^8"
    },
    "EIP7702-OBL-010": {
        "client_locations": "[core/types/tx_setcode.go:L77]",
        "client_code_flow": "RLP decode -> SetCodeAuthorization struct [L77: R uint256.Int] - uint256.Int enforces < 2^256"
    },
    "EIP7702-OBL-011": {
        "client_locations": "[core/types/tx_setcode.go:L78]",
        "client_code_flow": "RLP decode -> SetCodeAuthorization struct [L78: S uint256.Int] - uint256.Int enforces < 2^256"
    },
    "EIP7702-OBL-012": {
        "client_locations": "[core/state_transition.go:L503, core/state_transition.go:L506-L511]",
        "client_code_flow": "core/state_transition.go:execute() [L503: SetNonce(msg.From, nonce+1) increments sender nonce]; [L506-511: for loop processes msg.SetCodeAuthorizations via applyAuthorization() before evm.Call()]"
    },
    "EIP7702-OBL-013": {
        "client_locations": "[core/state_transition.go:L579-L581, core/error.go:L140]",
        "client_code_flow": "core/state_transition.go:validateAuthorization() [L579-581: if !auth.ChainID.IsZero() && auth.ChainID.CmpBig(chainConfig.ChainID) != 0 returns ErrAuthorizationWrongChainID]"
    },
    "EIP7702-OBL-014": {
        "client_locations": "[core/state_transition.go:L583-L585, core/error.go:L141]",
        "client_code_flow": "core/state_transition.go:validateAuthorization() [L583-585: if auth.Nonce+1 < auth.Nonce returns ErrAuthorizationNonceOverflow] - checks nonce < 2^64-1"
    },
    "EIP7702-OBL-015": {
        "client_locations": "[core/types/tx_setcode.go:L109-L139, core/types/tx_setcode.go:L118-L129]",
        "client_code_flow": "tx_setcode.go:Authority() [L118-139: computes SigHash() then crypto.Ecrecover]; SigHash() [L109-114: returns prefixedRlpHash(0x05, [ChainID, Address, Nonce])]"
    },
    "EIP7702-OBL-016": {
        "client_locations": "[core/types/tx_setcode.go:L120, crypto/crypto.go:L240-L251]",
        "client_code_flow": "tx_setcode.go:Authority() [L120: calls crypto.ValidateSignatureValues(a.V, R, S, true)]; crypto/crypto.go [L246: if homestead && s.Cmp(secp256k1halfN) > 0 return false]"
    },
    "EIP7702-OBL-017": {
        "client_locations": "[core/state_transition.go:L596]",
        "client_code_flow": "core/state_transition.go:validateAuthorization() [L596: st.state.AddAddressToAccessList(authority)] adds authority to accessed_addresses"
    },
    "EIP7702-OBL-018": {
        "client_locations": "[core/state_transition.go:L597-L600, core/types/tx_setcode.go:L37-L42]",
        "client_code_flow": "core/state_transition.go:validateAuthorization() [L597-600: if _, ok := types.ParseDelegation(code); len(code) != 0 && !ok returns ErrAuthorizationDestinationHasCode]; tx_setcode.go:ParseDelegation() [L37-42: checks 0xef0100 prefix]"
    },
    "EIP7702-OBL-019": {
        "client_locations": "[core/state_transition.go:L601-L603, core/error.go:L144]",
        "client_code_flow": "core/state_transition.go:validateAuthorization() [L601-603: if have := st.state.GetNonce(authority); have != auth.Nonce returns ErrAuthorizationNonceMismatch]"
    },
    "EIP7702-OBL-020": {
        "client_locations": "[core/state_transition.go:L616-L618, params/protocol_params.go:L37, params/protocol_params.go:L101]",
        "client_code_flow": "core/state_transition.go:applyAuthorization() [L616-618: if st.state.Exist(authority) adds refund CallNewAccountGas - TxAuthTupleGas]; params [L37: CallNewAccountGas=25000, L101: TxAuthTupleGas=12500]"
    },
    "EIP7702-OBL-021": {
        "client_locations": "[core/state_transition.go:L628-L629, core/types/tx_setcode.go:L45-L47, core/types/tx_setcode.go:L34]",
        "client_code_flow": "core/state_transition.go:applyAuthorization() [L628-629: st.state.SetCode(authority, types.AddressToDelegation(auth.Address))]; tx_setcode.go:AddressToDelegation() [L45-47: returns DelegationPrefix || address]; DelegationPrefix [L34: []byte{0xef, 0x01, 0x00}]"
    },
    "EIP7702-OBL-022": {
        "client_locations": "[core/state_transition.go:L622-L626]",
        "client_code_flow": "core/state_transition.go:applyAuthorization() [L622-626: if auth.Address == (common.Address{}) then st.state.SetCode(authority, nil) clears code]"
    },
    "EIP7702-OBL-023": {
        "client_locations": "[core/state_transition.go:L621]",
        "client_code_flow": "core/state_transition.go:applyAuthorization() [L621: st.state.SetNonce(authority, auth.Nonce+1)] increments authority nonce after setting delegation"
    },
    "EIP7702-OBL-024": {
        "client_locations": "[core/state_transition.go:L609-L612, core/state_transition.go:L506-L511]",
        "client_code_flow": "core/state_transition.go:applyAuthorization() [L609-612: if err := validateAuthorization() returns err without aborting tx]; execute() [L506-511: for loop ignores errors via st.applyAuthorization(&auth)]"
    },
    "EIP7702-OBL-025": {
        "client_locations": "[core/state_transition.go:L506-L511]",
        "client_code_flow": "core/state_transition.go:execute() [L506-511: for loop processes authorizations in order; each applyAuthorization() calls SetCode, so later valid authorizations overwrite earlier ones for same authority]"
    },
    "EIP7702-OBL-026": {
        "client_locations": "[core/state_transition.go:L506-L523, core/vm/evm.go:L257, core/vm/evm.go:L304-L306]",
        "client_code_flow": "core/state_transition.go:execute() [L506-511: applyAuthorization() modifies state before evm.Call()]; evm.go:Call() [L257: snapshot taken after auth processing; L304-306: revert to snapshot on error does NOT affect delegations set earlier]"
    },
    "EIP7702-OBL-027": {
        "client_locations": "[core/vm/evm.go:L628-L638, core/vm/evm.go:L289, core/vm/evm.go:L355, core/vm/evm.go:L399, core/vm/evm.go:L450]",
        "client_code_flow": "core/vm/evm.go:resolveCode() [L628-638: if ParseDelegation(code) ok, returns StateDB.GetCode(target)]; Call() [L289: code := evm.resolveCode(addr)]; CallCode() [L355: resolveCode(addr)]; DelegateCall() [L399: resolveCode(addr)]; StaticCall() [L450: resolveCode(addr)]"
    },
    "EIP7702-OBL-028": {
        "client_locations": "[core/vm/evm.go:L294-L297]",
        "client_code_flow": "evm.go:Call() [L294-297: contract.SetCallCode(resolveCodeHash(addr), code) where code is already resolved delegation target]; opcodes CODESIZE/CODECOPY operate on contract.Code which is the delegated code"
    },
    "EIP7702-OBL-029": {
        "client_locations": "[core/vm/evm.go:L285-L286, core/vm/evm.go:L258]",
        "client_code_flow": "evm.go:Call() [L258: p, isPrecompile := evm.precompile(addr)]; if address is precompile, handled separately [L285-286: RunPrecompiledContract]; delegation resolution only for non-precompiles so precompile-delegated code is empty"
    },
    "EIP7702-OBL-030": {
        "client_locations": "[core/vm/evm.go:L285-L286, core/vm/evm.go:L289-L299]",
        "client_code_flow": "evm.go:Call() [L285-286: if isPrecompile, runs precompile]; [L289-299: else resolveCode - if delegating to precompile, resolveCode returns precompile code but Call checks isPrecompile first on original addr, not delegated]"
    },
    "EIP7702-OBL-031": {
        "client_locations": "[core/vm/evm.go:L633-L636]",
        "client_code_flow": "evm.go:resolveCode() [L633-636: if target, ok := ParseDelegation(code); ok returns StateDB.GetCode(target)] - only ONE level of resolution, does not recurse"
    },
    "EIP7702-OBL-032": {
        "client_locations": "[core/state_transition.go:L71-L117, params/protocol_params.go:L38-L40, params/protocol_params.go:L99-L100]",
        "client_code_flow": "core/state_transition.go:IntrinsicGas() [L71-117: TxGas(21000) + data cost + accessList cost]; params [L38: TxGas=21000, L40: TxDataZeroGas=4, L99: TxAccessListAddressGas=2400, L100: TxAccessListStorageKeyGas=1900]"
    },
    "EIP7702-OBL-033": {
        "client_locations": "[core/state_transition.go:L113-L115, params/protocol_params.go:L37]",
        "client_code_flow": "core/state_transition.go:IntrinsicGas() [L113-115: if authList != nil adds len(authList) * CallNewAccountGas]; params [L37: CallNewAccountGas=25000 is PER_EMPTY_ACCOUNT_COST]"
    },
    "EIP7702-OBL-034": {
        "client_locations": "[core/state_transition.go:L113-L115]",
        "client_code_flow": "core/state_transition.go:IntrinsicGas() [L113-115: charges len(authList) * CallNewAccountGas] - uses len(authList) regardless of validity; validation happens later in applyAuthorization()"
    },
    "EIP7702-OBL-035": {
        "client_locations": "[core/vm/operations_acl.go:L274-L287, params/protocol_params.go:L68]",
        "client_code_flow": "core/vm/operations_acl.go:makeCallVariantGasCallEIP7702() [L274-287: if !AddressInAccessList(target) charges ColdAccountAccessCostEIP2929 and adds to access list]; params [L68: ColdAccountAccessCostEIP2929=2600]"
    },
    "EIP7702-OBL-036": {
        "client_locations": "[core/vm/operations_acl.go:L277-L279, params/protocol_params.go:L70]",
        "client_code_flow": "core/vm/operations_acl.go:makeCallVariantGasCallEIP7702() [L277-279: if AddressInAccessList(target) charges WarmStorageReadCostEIP2929]; params [L70: WarmStorageReadCostEIP2929=100]"
    },
    "EIP7702-OBL-037": {
        "client_locations": "[core/state_transition.go:L334-L338, core/types/tx_setcode.go:L37-L42]",
        "client_code_flow": "core/state_transition.go:preCheck() [L334-338: if _, delegated := types.ParseDelegation(code); len(code) > 0 && !delegated returns ErrSenderNoEOA]; ParseDelegation() [L37-42: valid if len==23 && HasPrefix(DelegationPrefix)]"
    },
    "EIP7702-OBL-038": {
        "client_locations": "[core/state_transition.go:L334-L338, core/error.go:L110]",
        "client_code_flow": "core/state_transition.go:preCheck() [L334-338: if len(code) > 0 && !delegated returns ErrSenderNoEOA]; core/error.go [L110: ErrSenderNoEOA = 'sender not an eoa']"
    },
    "EIP7702-OBL-039": {
        "client_locations": "[core/state_transition.go:L518-L520]",
        "client_code_flow": "core/state_transition.go:execute() [L518-520: if addr, ok := types.ParseDelegation(GetCode(*msg.To)); ok then AddAddressToAccessList(addr)] adds delegation target to access list"
    },
    "EIP7702-OBL-040": {
        "client_locations": "[core/types/receipt.go:L121-L141, core/types/receipt.go:L138-L141]",
        "client_code_flow": "core/types/receipt.go:EncodeRLP() [L123-135: for typed tx writes type byte prefix then RLP data]; encodeTyped() [L138-141: w.WriteByte(r.Type) then rlp.Encode(receiptRLP)] - receiptRLP has [status, cumGasUsed, bloom, logs]"
    },
}

def main():
    # Read input CSV
    with open(INPUT_CSV, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # Add new columns
    new_fieldnames = fieldnames + ['client_locations', 'client_code_flow', 'client_obligation_gap', 'client_code_gap']

    # Process each row
    for row in rows:
        obl_id = row['id']
        if obl_id in GETH_MAPPINGS:
            mapping = GETH_MAPPINGS[obl_id]
            row['client_locations'] = mapping['client_locations']
            row['client_code_flow'] = mapping['client_code_flow']
        else:
            row['client_locations'] = ''
            row['client_code_flow'] = ''
        row['client_obligation_gap'] = ''
        row['client_code_gap'] = ''

    # Write output CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")

if __name__ == '__main__':
    main()
