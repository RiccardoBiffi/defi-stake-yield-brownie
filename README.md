# Preview the project here: https://riccardobiffi.github.io/

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

- We allow 3 tokens initially:
    - RWD (the reward token)
    - WETH
    - DAI (as fau_token for testing purposes)

- Usually the front_end stays on an other repository. We keep it here becouse it's simple enough
    - node_module will be ignored
    - public folder contains index.html, images and manifest
    - src is where we work
    - the first time, install all packages with > yarn
    - To start the front-end (from a script), > yarn start

- We use React + MUI v5 with Emotion.

- We need to send the chain IDs and the contracts address to the front-end to connect with them.
    - We copy the brownie-config file for static addresses
    - We copy the build folder for dynamic addresses (eg. my deployed contracts)

- An hook is like a component but more functionality-oriented
