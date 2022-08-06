import React from 'react';
import ReactDOM from 'react-dom'

import { Rinkeby, DAppProvider, Config } from '@usedapp/core'
import { formatEther } from '@ethersproject/units'
import { getDefaultProvider } from 'ethers'
import { Header } from './components/Header'

const config: Config = {
  readOnlyChainId: Rinkeby.chainId,
  readOnlyUrls: {
    [Rinkeby.chainId]: getDefaultProvider('rinkeby'),
  },
}

function App() {
  return (
    <DAppProvider config={config}>
      <Header />
      <div>Hi!</div>
    </DAppProvider>
  );
}

export default App;
