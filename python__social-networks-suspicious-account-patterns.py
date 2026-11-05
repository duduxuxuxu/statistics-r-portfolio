# Selected student implementation excerpts. Original course framework and instructor-provided docstrings are omitted.
# These excerpts retain the saved implementation bodies and require their course framework to run.
from __future__ import annotations

def _collect_numeric_values(users_dict: UserData, key: str) -> list[int]:
    values: list[int] = []
    for account in users_dict.values():
        if key in account:
            values.append(account[key])
    return values

def _add_group(account: AccountData, group_name: str) -> None:
    if group_name not in account[BOT_GROUPS]:
        account[BOT_GROUPS].append(group_name)

def _is_recent_account(account_created: str) -> bool:
    return account_created > RECENT_ACCOUNT_CUTOFF

def _bot_candidate_names(users_dict: UserData) -> set[str]:
    return {
        username
        for username, account in users_dict.items()
        if BOT_GROUPS in account and account[BOT_GROUPS]
    }

def _count_bot_followers(account: AccountData, bot_set: set[str]) -> int:
    return sum(1 for follower in account[FOLLOWERS] if follower in bot_set)

def create_users_dictionary(users_file: TextIO) -> UserData:
    users_dict: UserData = {}

    # Discard header if the file pointer is at the start.
    users_file.readline()

    for raw_line in users_file:
        line = raw_line.strip()
        if not line:
            continue

        columns = line.split(SEP)
        username = columns[USERNAME_COL]

        if username in users_dict:
            continue

        users_dict[username] = {
            DOB: columns[DOB_COL],
            NUM_POSTS: int(columns[NUM_POSTS_COL]),
            NUM_COMMENTS: int(columns[NUM_COMMENTS_COL]),
            ACCOUNT_CREATED: columns[ACCOUNT_CREATED_COL],
            FOLLOWERS: [],
            FOLLOWING: [],
            BOT_GROUPS: [],
        }

    return users_dict

def add_followers(users_dict: UserData, followers_file: TextIO) -> None:
    followers_file.readline()

    for raw_line in followers_file:
        line = raw_line.strip()
        if not line:
            continue

        columns = line.split(SEP)
        follower = columns[FOLLOWER_COL]
        following = columns[FOLLOWING_COL]

        if follower not in users_dict or following not in users_dict:
            continue

        followers_list = users_dict[following][FOLLOWERS]
        if follower not in followers_list:
            followers_list.append(follower)

        following_list = users_dict[follower][FOLLOWING]
        if following not in following_list:
            following_list.append(following)

def add_num_mutual_connections(users_dict: UserData) -> None:
    for account in users_dict.values():
        followers = set(account.get(FOLLOWERS, []))
        following = set(account.get(FOLLOWING, []))
        account[NUM_MUTUALS] = len(followers.intersection(following))

def get_quantile(values: list[int], p: float) -> int:
    if not values or not 0.0 <= p <= 1.0:
        return -1

    sorted_values = sorted(values)
    if p == 1.0:
        return sorted_values[-1]

    if len(sorted_values) == 1:
        return sorted_values[0]

    index = int(p * (len(sorted_values) - 1))
    return sorted_values[index]

def _compute_bot_thresholds(
    users_dict: UserData,
) -> tuple[int, int, int, int, int]:
    comment_values = _collect_numeric_values(users_dict, NUM_COMMENTS)
    post_values = _collect_numeric_values(users_dict, NUM_POSTS)
    mutual_values = _collect_numeric_values(users_dict, NUM_MUTUALS)

    comment_hclp = (
        get_quantile(comment_values, P_HCLP_COMMENT)
        if comment_values else -1
    )
    post_hclp = (
        get_quantile(post_values, P_HCLP_POSTS)
        if post_values else -1
    )
    comment_hclm = (
        get_quantile(comment_values, P_HCLM_COMMENT)
        if comment_values else -1
    )
    mutual_hclm = (
        get_quantile(mutual_values, P_HCLM_MUTUALS)
        if mutual_values else -1
    )
    comment_hcna = (
        get_quantile(comment_values, P_HCNA_COMMENT)
        if comment_values else -1
    )

    return comment_hclp, post_hclp, comment_hclm, mutual_hclm, comment_hcna

def _tag_account_with_bot_groups(
    account: AccountData, thresholds: tuple[int, int, int, int, int]
) -> None:
    (
        comment_hclp,
        post_hclp,
        comment_hclm,
        mutual_hclm,
        comment_hcna,
    ) = thresholds

    num_comments = account[NUM_COMMENTS]
    num_posts = account[NUM_POSTS]
    num_mutuals = account.get(NUM_MUTUALS, 0)

    if (
        comment_hclp != -1
        and post_hclp != -1
        and num_comments >= comment_hclp
        and num_posts <= post_hclp
    ):
        _add_group(account, HCLP)

    if (
        comment_hclm != -1
        and mutual_hclm != -1
        and num_comments >= comment_hclm
        and num_mutuals <= mutual_hclm
    ):
        _add_group(account, HCLM)

    if (
        comment_hcna != -1
        and num_comments >= comment_hcna
        and _is_recent_account(account[ACCOUNT_CREATED])
    ):
        _add_group(account, HCNA)

    followers_count = len(account[FOLLOWERS])
    following_count = len(account[FOLLOWING])
    if followers_count * HFLF_FACTOR < following_count:
        _add_group(account, HFLF)

def add_bot_candidate_groups(users_dict: UserData) -> None:
    if not users_dict:
        return

    thresholds = _compute_bot_thresholds(users_dict)

    for account in users_dict.values():
        _tag_account_with_bot_groups(account, thresholds)

def find_all_bot_candidates(users_dict: UserData) -> UserData:
    return {
        username: deepcopy(account)
        for username, account in users_dict.items()
        if account[BOT_GROUPS]
    }

def find_users_abusing_system(users_dict: UserData) -> UserData:
    bot_set = _bot_candidate_names(users_dict)
    result: UserData = {}

    for username, account in users_dict.items():
        followers = account[FOLLOWERS]
        if not followers:
            continue
        bot_followers = _count_bot_followers(account, bot_set)
        if bot_followers > len(followers) / 2:
            result[username] = deepcopy(account)

    return result

def order_bot_candidates(users_dict: UserData) -> list[str]:
    candidates = [
        username
        for username, account in users_dict.items()
        if account[BOT_GROUPS]
    ]

    return sorted(
        candidates,
        key=lambda name: (len(users_dict[name][BOT_GROUPS]), name),
        reverse=True,
    )

def order_users_abusing_system(users_dict: UserData) -> list[str]:
    bot_set = _bot_candidate_names(users_dict)
    abusive_counts: dict[str, int] = {}

    for username, account in users_dict.items():
        followers = account[FOLLOWERS]
        if not followers:
            continue
        bot_followers = _count_bot_followers(account, bot_set)
        if bot_followers > len(followers) / 2:
            abusive_counts[username] = bot_followers

    return sorted(
        abusive_counts,
        key=lambda name: (abusive_counts[name], name),
        reverse=True,
    )
