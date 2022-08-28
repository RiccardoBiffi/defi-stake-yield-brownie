import { Box, Button, Container, Tab } from "@mui/material";
import { TabContext, TabList, TabPanel } from "@mui/lab";
import { Token } from "../Main";
import React, { useState } from "react";
import { WalletBalance } from "./WalletBalance";
import { StakeBalance } from "./StakeBalance";
import { Reward } from "./Reward";
import { StakeForm } from "./StakeForm";
import { UnstakeForm } from "./UnstakeForm";
import styled from "@emotion/styled";
import { MoreActionsAndInfo } from "./MoreActionsAndInfo";

const TabContainerBackground = styled(Container)`
    padding: 4px!important;
    border-radius: 30px;
    background: linear-gradient(-23deg, hsl(237, 61%, 15%), hsl(188, 61%, 30%), hsl(136, 39%, 37%));
    box-shadow: 0px 4px 25px 0px #00000088;
`
const TabContainer = styled(Box)`
    background-color: white;
    border-radius: 25px;
    flex-basis: 100%;
`
const TabListBorder = styled(TabList)`
  border-bottom: 1px solid lightgray;
`
const UnstakeAllButton = styled(Button)`
    margin: 3px 20px 3px auto;
    border: 2px solid #1976d2 !important;
    border-radius: 8px;
    font-weight: bold;
`
const TabContent = styled.div`
    flex-direction: column;
    align-items: center;
    display: inline-flex;
    flex: 1 1 0px;
`
const BoxFlex = styled(Box)`
    display: flex;
    flex-wrap: wrap;
    justify-content: end;
`
const VerticalLine = styled.div`
    width: 4px;
    background: linear-gradient(135deg, hsl(237, 61%, 15%), hsl(188, 61%, 30%), hsl(136, 39%, 37%));
    border-radius: 10px;
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
    <BoxFlex>
      <Reward token={
        supportedTokens.find(token => {
          return token.name === "RWD";
        }
        )} />
      <TabContainerBackground>
        <TabContainer>
          <TabContext value={selectedTokenIndex.toString()}>
            <TabListBorder onChange={handleChange} aria-label="stake form tabs">
              {supportedTokens.map((token, i) => {
                return (
                  <Tab
                    label={token.name}
                    value={i.toString()}
                    key={i} />
                )
              })}
              <UnstakeAllButton>Unstake all</UnstakeAllButton>
            </TabListBorder>
            {supportedTokens.map((token, i) => {
              return (
                <TabPanel value={i.toString()} key={i}>
                  <BoxFlex>
                    <TabContent>
                      <WalletBalance token={token} />
                      <StakeForm token={token} />
                    </TabContent>
                    <VerticalLine />
                    <TabContent>
                      <StakeBalance token={token} />
                      <UnstakeForm token={token} />
                    </TabContent>
                  </BoxFlex>
                  <MoreActionsAndInfo token={token} />
                </TabPanel>
              )
            })}
          </TabContext>
        </TabContainer>
      </TabContainerBackground>

    </BoxFlex>
  )
}