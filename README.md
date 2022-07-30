- We have a reward token.
- We have a contract to un/stake token, issue tokens, allow tokens and get ETH value

- to stake a token, we must
    - have a list of allowed token (managed by admins)
    - have a list of stakers
    - a mapping with what token - a given staker - for what amount has staked
    - how many token types a staker has staked

- To issue the reward token, we must know the TVL of the user.
    - We compute it by looping throught the allowed tokens.
    - Every time the user owns it, we get its price feed * amount and get its total vale
    - we need a mapping with what taken - it's chainlink priceFeed
    - The summation of each token total value is the TVL 