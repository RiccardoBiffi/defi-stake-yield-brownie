import { Goerli, useEthers } from "@usedapp/core";
import helper from "../helper-config.json";
import networkMapping from "../chain_info/deployments/map.json";
import { constants } from "ethers";
import brownieConfig from "../brownie-config.json";
import rwd from "../images/dapp.png";
import eth from "../images/eth.png";
import dai from "../images/dai.png";
import { YourWallet } from "./yourWallet/YourWallet";
import styled from "@emotion/styled";

const Title = styled.h1`
  color: white;
  text-align: center;
  padding: 8px;
`;

const Connect = styled.h2`
  color: white;
  text-align: center;
  padding: 8px;
  text-decoration: underline;
`;

export type Token = {
  image: string;
  address: string;
  name: string;
};

export const Main = () => {
  const { account, chainId } = useEthers();
  const network = chainId ? helper[chainId] : "dev";
  const isConnected = !!account;
  const isCorrectChain = chainId === Goerli.chainId;

  let supportedTokens: Array<Token> = [];

  if (isCorrectChain) {
    const rewardTokenAddress = chainId
      ? networkMapping[String(chainId)]["RewardToken"][0]
      : constants.AddressZero;
    const wethTokenAddress = chainId
      ? brownieConfig["networks"][network]["weth_token"]
      : constants.AddressZero;
    const daiTokenAddress = chainId
      ? brownieConfig["networks"][network]["fau_token"]
      : constants.AddressZero;
    // const tokenFarmAddress = chainId ?
    //     networkMapping[String(chainId)]["TokenFarm"][0] :
    //     constants.AddressZero;
    // const ethUsdFeedAddress = chainId ?
    //     brownieConfig["networks"][network]["eth_usd_feed"] :
    //     constants.AddressZero;
    // const daiUsdFeedAddress = chainId ?
    //     brownieConfig["networks"][network]["dai_usd_feed"] :
    //     constants.AddressZero;

    supportedTokens = [
      {
        image: rwd,
        address: rewardTokenAddress,
        name: "RWD",
      },
      {
        image: eth,
        address: wethTokenAddress,
        name: "WETH",
      },
      {
        image: dai,
        address: daiTokenAddress,
        name: "DAI",
      },
    ];
  }

  return (
    <>
      <Title>Dapp Token App</Title>
      {isConnected && isCorrectChain ? (
        <YourWallet supportedTokens={supportedTokens} />
      ) : (
        <Connect>
          {isCorrectChain
            ? "Please connect your wallet"
            : "Please switch network and then connect your wallet"}
        </Connect>
      )}
    </>
  );
};
