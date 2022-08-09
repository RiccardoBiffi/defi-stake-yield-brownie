import { Box, Tab } from "@mui/material";
import { TabContext, TabList, TabPanel } from "@mui/lab";
import { Token } from "../Main";
import React, { useState } from "react";
import { WalletBalance } from "./WalletBalance";
import { StakeForm } from "./StakeForm";

interface YourWalletProps {
  supportedTokens: Array<Token>;
}

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
  // state hook: create variable and its setter as a component state
  const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0);
  const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
    setSelectedTokenIndex(parseInt(newValue));
  }

  return (
    <Box>
      <h1>Your wallet!</h1>
      <Box>
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
                <div>
                  <WalletBalance token={token} />
                  <StakeForm token={token} />
                </div>
              </TabPanel>
            )
          })}
        </TabContext>
      </Box>
    </Box>

  )
}