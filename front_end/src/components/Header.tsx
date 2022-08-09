import { useEthers } from "@usedapp/core";
import { Button } from "@mui/material";
import styled from "@emotion/styled"


const Container = styled.div`
    padding: 8px;
    display: flex;
    justify-content: flex-end;
`
export const Header = () => {
  const { account, activateBrowserWallet, deactivate } = useEthers();
  const isConnected = account !== undefined;

  return (
    <Container >
      <div>
        {isConnected ? (
          <Button color="primary" variant="contained"
            onClick={() => deactivate()}>Disconnect</Button>
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