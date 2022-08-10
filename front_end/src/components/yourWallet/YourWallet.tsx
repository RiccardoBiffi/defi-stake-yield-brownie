import { Box, Tab } from "@mui/material";
import { TabContext, TabList, TabPanel } from "@mui/lab";
import { Token } from "../Main";
import React, { useState } from "react";
import { WalletBalance } from "./WalletBalance";
import { StakeForm } from "./StakeForm";
import styled from "@emotion/styled";

const TabContent = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 8px;
`
const Header = styled.h1`
    color: white;
`
const TabContainer = styled(Box)`
    background-color: white;
    border-radius: 25px;
`

interface YourWalletProps {
  supportedTokens: Array<Token>;
}

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
  // state hook: create variable and its setter as a component state
  const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0); // default is 0
  const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
    setSelectedTokenIndex(parseInt(newValue));
  }

  return (
    <Box>
      <Header>Your wallet!</Header>
      <TabContainer>
        <TabContext value={selectedTokenIndex.toString()}>
          <TabList onChange={handleChange} aria-label="stake form tabs">
            {supportedTokens.map((token, i) => {
              return (
                <Tab
                  label={token.name}
                  value={i.toString()}
                  key={i} />
              )
            })}
          </TabList>
          {supportedTokens.map((token, i) => {
            return (
              <TabPanel value={i.toString()} key={i}>
                <TabContent>
                  <WalletBalance token={token} />
                  <StakeForm token={token} />
                </TabContent>
              </TabPanel>
            )
          })}
        </TabContext>
      </TabContainer>
    </Box>

  )
}