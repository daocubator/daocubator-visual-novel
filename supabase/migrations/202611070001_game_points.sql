-- Get Rich Together milestone points.
-- A user can only receive each milestone once. The server chooses point values;
-- the client sends milestone identifiers, never a requested point amount.

create table if not exists public.game_point_events (
    user_id uuid not null references auth.users (id) on delete cascade,
    milestone_id text not null,
    points integer not null check (points > 0),
    created_at timestamptz not null default now(),
    primary key (user_id, milestone_id)
);

alter table public.game_point_events enable row level security;
revoke all on table public.game_point_events from anon, authenticated;

create or replace function public.award_game_milestones(p_milestone_ids text[])
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
    v_user_id uuid := auth.uid();
    v_milestone_id text;
    v_glossary_id text;
    v_points integer;
    v_inserted integer;
    v_new_awards integer := 0;
    v_balance integer;
    v_glossary_ids constant text[] := array[
        'vibes', 'security', 'morale', 'dao', 'governance', 'governance_token',
        'proposal', 'turnout', 'quorum', 'delegation', 'veto', 'timelock',
        'multisig', 'attack51', 'capture', 'fork', 'decentralization', 'whale',
        'legal_wrapper', 'general_partnership', 'blockchain', 'genesis_block',
        'token', 'tokenomics', 'tge', 'mint', 'burn', 'eth', 'gas', 'wallet',
        'hot_wallet', 'cold_storage', 'hardware_wallet', 'seed_phrase',
        'private_key', 'smart_contract', 'solidity', 'bytecode', 'reentrancy',
        'audit', 'address', 'hex', 'phishing', 'ice_phishing', 'token_approval',
        'front_end', 'cdn', 'malware', 'pfp', 'key_rotation', 'test_transaction',
        'custodial', 'escrow', 'defi', 'treasury', 'native_token', 'stablecoin',
        'barbell', 'swap_fee', 'death_spiral', 'flash_loan', 'bear_market',
        'candle', 'number_go_up', 'carbon_credit', 'greenwashing', 'equity',
        'equal_split', 'vesting', 'cliff', 'dead_equity', 'cap_table', 'cofounder',
        'board_seat', 'runway', 'payroll', 'deferred_salary', 'moat', 'standup',
        'postmortem', 'burnout', 'exit', 'acquisition', 'unicorn', 'regulator',
        'due_diligence', 'advance', 'recoupment', 'deal_360', 'cross_collat',
        'masters', 'preorder', 'validation', 'cut_and_sew', 'unit_cost',
        'overfunding', 'chargeback', 'payment_processor'
    ];
begin
    if v_user_id is null then
        raise exception 'Sign in is required to sync game points.' using errcode = '28000';
    end if;

    foreach v_milestone_id in array coalesce(p_milestone_ids, array[]::text[]) loop
        v_points := null;

        if v_milestone_id = 'scenario:ep1_keys:cleared'
           or v_milestone_id = 'scenario:ep2_lisbon:cleared'
           or v_milestone_id = 'scenario:ep3_agreements:cleared'
           or v_milestone_id = 'scenario:ep4_apothecary:cleared' then
            v_points := 300;
        elsif v_milestone_id like 'glossary:discovered:%'
           or v_milestone_id like 'glossary:explored:%' then
            v_glossary_id := split_part(v_milestone_id, ':', 3);
            if array_length(string_to_array(v_milestone_id, ':'), 1) = 3
               and v_glossary_id = any (v_glossary_ids) then
                v_points := 10;
            end if;
        end if;

        if v_points is not null then
            insert into public.game_point_events (user_id, milestone_id, points)
            values (v_user_id, v_milestone_id, v_points)
            on conflict (user_id, milestone_id) do nothing;
            get diagnostics v_inserted = row_count;
            v_new_awards := v_new_awards + v_inserted;
        end if;
    end loop;

    select coalesce(sum(points), 0)::integer
      into v_balance
      from public.game_point_events
     where user_id = v_user_id;

    return jsonb_build_object('points', v_balance, 'new_awards', v_new_awards);
end;
$$;

create or replace function public.get_game_points()
returns integer
language sql
stable
security definer
set search_path = ''
as $$
    select coalesce(sum(points), 0)::integer
      from public.game_point_events
     where user_id = auth.uid();
$$;

revoke all on function public.award_game_milestones(text[]) from public, anon;
revoke all on function public.get_game_points() from public, anon;
grant execute on function public.award_game_milestones(text[]) to authenticated;
grant execute on function public.get_game_points() to authenticated;
