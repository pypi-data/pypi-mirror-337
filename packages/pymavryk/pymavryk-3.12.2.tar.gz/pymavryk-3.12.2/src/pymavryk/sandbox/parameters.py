from typing import Any
from typing import Dict

from pymavryk.crypto.key import Key

ATLAS = 'PtAtLasomUEW99aVhVTrqjCHjJSpFUa8uHNEAEamx9v2SNeTaNp'
BOREAS = 'PtBzwViMCC1gfm98y5TDKqz2e3vjBXPAUoWu7jfEcN6yj2ZhCyT'
LATEST = BOREAS

protocol_hashes = {
    'atlas': ATLAS,
    'boreas': BOREAS,
}

protocol_version = {
    ATLAS: 1,
    BOREAS: 2,
}

sandbox_commitment = {
    "mnemonic": [
        "arctic",
        "blame",
        "brush",
        "economy",
        "solar",
        "swallow",
        "canvas",
        "live",
        "vote",
        "two",
        "post",
        "neutral",
        "spare",
        "split",
        "fall",
    ],
    "activation_code": "7375ef222cc038001b6c8fb768246c86e994745b",
    "amount": "38323962971",
    "pkh": "mv1JVZzbrGpKfripWo2GiWZ7wkzoeKHna498",
    "password": "ZuPOpZgMNM",
    "email": "nbhcylbg.xllfjgrk@tezos.example.org",
}

sandbox_addresses = {
    'activator': 'mv1FeNQ3gSZoEFp1mr6VTLnMqV5tuNwHTgw5',
    'bootstrap5': 'mv1S14SxfuavHMGDXxZJoBERZafLTyX3Z6Dx',
    'bootstrap4': 'mv1PVMnW8iyYxCoqLfPAha8EAPRxjTx7wqbn',
    'bootstrap3': 'mv1TxMEnmav51G1Hwcib1rBnBeniDMgG8nkJ',
    'bootstrap2': 'mv1V73YiKvinVumxwvYWjCZBoT44wqBNhta7',
    'bootstrap1': 'mv18Cw7psUrAAPBpXYd9CtCpHg9EgjHP9KTe',
}

sandbox_params: Dict[str, Any] = {
    # NOTE: Built-in accounts
    'bootstrap_accounts': [
        ['edpkuBknW28nW72KG6RoHtYW7p12T6GKc7nAbwYX5m8Wd9sDVC9yav', '4000000000000'],
        ['edpktzNbDAUjUk697W7gYg2CRuBQjyPxbEg8dLccYYwKSKvkPvjtV9', '4000000000000'],
        ['edpkuTXkJDGcFd5nh6VvMz8phXxU3Bi7h6hqgywNFi1vZTfQNnS1RV', '4000000000000'],
        ['edpkuFrRoDSEbJYgxRtLx2ps82UdaYc1WwfS9sE11yhauZt5DgCHbU', '4000000000000'],
        ['edpkv8EUUH68jmo3f7Um5PezmfGrRF24gnfLpH3sVNwJnV5bVCxL2n', '4000000000000'],
    ],
    'bootstrap_contracts': [],
    'commitments': [
        [
            Key.from_faucet(sandbox_commitment).blinded_public_key_hash(),
            '100500000000',
        ],
    ],
    # NOTE: Shorter cycles, voting periods and other parameters
    # NOTE: From https://gitlab.com/tezos/tezos/-/blob/master/src/proto_019_PtParisB/lib_parameters/default_parameters.ml#L317
    'blocks_preservation_cycles': 1,
    'consensus_rights_delay': 2,
    'delegate_parameters_activation_delay': 2,
    'blocks_per_cycle': 8,
    'blocks_per_commitment': 4,
    'nonce_revelation_threshold': 4,
    'cycles_per_voting_period': 8,
    'proof_of_work_threshold': str((1 << 63) - 1),
    'vdf_difficulty': '50000',
    'minimal_block_delay': '1',
    'delay_increment_per_round': '1',
    'consensus_committee_size': 256,
    'consensus_threshold': 0,
    'limit_of_delegation_over_baking': 19,
    'max_operations_time_to_live': 8,
}

# NOTE: https://rpc.tzkt.io/boreasnet/chains/main/blocks/head/context/constants/parametric
boreas_params = {
    "consensus_rights_delay": 2,
    "blocks_preservation_cycles": 1,
    "delegate_parameters_activation_delay": 5,
    "blocks_per_cycle": 12288,
    "blocks_per_commitment": 96,
    "nonce_revelation_threshold": 768,
    "cycles_per_voting_period": 1,
    "hard_gas_limit_per_operation": "1040000",
    "hard_gas_limit_per_block": "1733333",
    "proof_of_work_threshold": "-1",
    "minimal_stake": "6000000000",
    "minimal_frozen_stake": "600000000",
    "vdf_difficulty": "10000000000",
    "origination_size": 257,
    "issuance_weights": {
        "base_total_issued_per_minute": "80007812",
        "baking_reward_fixed_portion_weight": 5120,
        "baking_reward_bonus_weight": 5120,
        "attesting_reward_weight": 10240,
        "seed_nonce_revelation_tip_weight": 1,
        "vdf_revelation_tip_weight": 1,
    },
    "cost_per_byte": "250",
    "hard_storage_limit_per_operation": "60000",
    "quorum_min": 2000,
    "quorum_max": 7000,
    "min_proposal_quorum": 500,
    "liquidity_baking_subsidy": "5000000",
    "liquidity_baking_toggle_ema_threshold": 1000000000,
    "max_operations_time_to_live": 360,
    "minimal_block_delay": "5",
    "delay_increment_per_round": "2",
    "consensus_committee_size": 7000,
    "consensus_threshold": 4667,
    "minimal_participation_ratio": {"numerator": 2, "denominator": 3},
    "limit_of_delegation_over_baking": 9,
    "percentage_of_frozen_deposits_slashed_per_double_baking": 500,
    "percentage_of_frozen_deposits_slashed_per_double_attestation": 5000,
    "max_slashing_per_block": 10000,
    "max_slashing_threshold": 2334,
    "testnet_dictator": "tz1Xf8zdT3DbAX9cHw3c3CXh79rc4nK4gCe8",
    "cache_script_size": 100000000,
    "cache_stake_distribution_cycles": 8,
    "cache_sampler_state_cycles": 8,
    "dal_parametric": {
        "feature_enable": True,
        "incentives_enable": False,
        "number_of_slots": 32,
        "attestation_lag": 8,
        "attestation_threshold": 66,
        "redundancy_factor": 8,
        "page_size": 3967,
        "slot_size": 126944,
        "number_of_shards": 512,
    },
    "smart_rollup_arith_pvm_enable": False,
    "smart_rollup_origination_size": 6314,
    "smart_rollup_challenge_window_in_blocks": 241920,
    "smart_rollup_stake_amount": "10000000000",
    "smart_rollup_commitment_period_in_blocks": 180,
    "smart_rollup_max_lookahead_in_blocks": 518400,
    "smart_rollup_max_active_outbox_levels": 241920,
    "smart_rollup_max_outbox_messages_per_level": 100,
    "smart_rollup_number_of_sections_in_dissection": 32,
    "smart_rollup_timeout_period_in_blocks": 120960,
    "smart_rollup_max_number_of_cemented_commitments": 5,
    "smart_rollup_max_number_of_parallel_games": 32,
    "smart_rollup_reveal_activation_level": {
        "raw_data": {"Blake2B": 0},
        "metadata": 0,
        "dal_page": 8193,
        "dal_parameters": 8193,
        "dal_attested_slots_validity_lag": 241920,
    },
    "smart_rollup_private_enable": True,
    "smart_rollup_riscv_pvm_enable": False,
    "zk_rollup_enable": False,
    "zk_rollup_origination_size": 4000,
    "zk_rollup_min_pending_to_process": 10,
    "zk_rollup_max_ticket_payload_size": 2048,
    "global_limit_of_staking_over_baking": 5,
    "edge_of_staking_over_delegation": 2,
    "adaptive_issuance_launch_ema_threshold": 0,
    "adaptive_rewards_params": {
        "issuance_ratio_final_min": {"numerator": "1", "denominator": "400"},
        "issuance_ratio_final_max": {"numerator": "1", "denominator": "10"},
        "issuance_ratio_initial_min": {"numerator": "9", "denominator": "200"},
        "issuance_ratio_initial_max": {"numerator": "11", "denominator": "200"},
        "initial_period": 10,
        "transition_period": 50,
        "max_bonus": "50000000000000",
        "growth_rate": {"numerator": "1", "denominator": "25"},
        "center_dz": {"numerator": "1", "denominator": "2"},
        "radius_dz": {"numerator": "1", "denominator": "50"},
    },
    "adaptive_issuance_activation_vote_enable": True,
    "autostaking_enable": True,
    "adaptive_issuance_force_activation": False,
    "ns_enable": True,
    "direct_ticket_spending_enable": False,
}


def get_protocol_parameters(protocol_hash: str) -> Dict[str, Any]:
    # https://gitlab.com/tezos/tezos/-/blob/master/src/proto_001_PtAtLas/lib_parameters/default_parameters.ml
    return {
        **boreas_params,
        # **old_params,
        **sandbox_params,
    }
