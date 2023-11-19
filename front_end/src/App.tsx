import { Kovan, DAppProvider, Config } from "@usedapp/core";
import { getDefaultProvider } from "ethers";
import { Header } from "./components/Header";
import { Main } from "./components/Main";
import { Container } from "@mui/material";

// todo refactor to include ganache (chain id 1337)
const config: Config = {
  readOnlyChainId: Kovan.chainId,
  readOnlyUrls: {
    [Kovan.chainId]: getDefaultProvider("kovan"),
  },
  notifications: {
    expirationPeriod: 1000,
    checkInterval: 1000,
  },
};

function App() {
  return (
    <DAppProvider config={config}>
      <Container maxWidth="lg">
        <Header />
        <Main />
      </Container>
    </DAppProvider>
  );
}

export default App;
