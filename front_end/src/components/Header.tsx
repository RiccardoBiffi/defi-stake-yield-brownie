import { useEthers } from "@usedapp/core";
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
`

export const Header = () => {
  const { account, activateBrowserWallet, deactivate } = useEthers();
  const isConnected = account !== undefined;

  return (
    <Container >
      <div>
        {isConnected ? (
          <>
            <Account
              color="primary"
              variant="contained"
              disabled
            >
              {account}
            </Account>
            <Button
              color="primary"
              variant="contained"
              onClick={() => deactivate()}>
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