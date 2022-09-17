import { Goerli, useEthers } from "@usedapp/core";
import { Button } from "@mui/material";
import styled from "@emotion/styled"

const Container = styled.div`
    padding: 8px;
    display: flex;
    justify-content: flex-end;
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
    <Container >
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
    </Container >
  )
}