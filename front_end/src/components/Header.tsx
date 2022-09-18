import { Goerli, useEthers } from "@usedapp/core";
import { Button } from "@mui/material";
import styled from "@emotion/styled"

const Container = styled.div`
    display: flex;
    padding: 12px 4px;
`

const Title = styled.div`
    font-size: 27px;
    color: white;
    padding: 8px;
    font-weight: bold;
`

const Connection = styled.div`
    padding: 8px 0;
    margin-left: auto;
`

const Account = styled(Button)`
    margin-right: 8px;
    color: white !important;
    background-color: #1976d2 !important;
    text-transform: initial;
`

export const Header = () => {
  const { account, activateBrowserWallet, deactivate, switchNetwork, chainId } = useEthers();
  const isConnected = !!account;
  const isCorrectChain = chainId === Goerli.chainId;

  const prettyPrint = (address: string) => {
    return address.slice(0, 6) + "..." + address.slice(address.length - 4, address.length);
  }

  return (
    <Container>
      <Title>Dapp Token App</Title>
      <Connection>
        <div>
          {!isCorrectChain ?
            (
              <Button
                color="primary"
                variant="contained"
                onClick={() => switchNetwork(Goerli.chainId)}>
                Switch to {Goerli.chainName}
              </Button>
            )
            :
            isConnected ? (
              <>
                <Account
                  color="primary"
                  variant="contained"
                  disabled
                >
                  {prettyPrint(account)}
                </Account>
                <Button
                  color="primary"
                  variant="contained"
                  onClick={deactivate}>
                  Disconnect
                </Button>

              </>
            )
              : (
                <Button color="primary" variant="contained"
                  onClick={() => activateBrowserWallet()}>
                  Connect
                </Button>
              )
          }
        </div>
      </Connection>
    </Container>
  )
}