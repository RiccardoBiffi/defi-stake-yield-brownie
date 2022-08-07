import { useEthers } from "@usedapp/core";
import styled from "@emotion/styled";
import helper from "../helper-config.json";
import networkMapping from "../chain_info/deployments/map.json"
import { constants } from "ethers";
import brownieConfig from "../brownie-config.json";
import rwd from "../dapp.png";
import eth from "../eth.png";
import dai from "../dai.png";

export type Token = {
    image: string;
    address: string;
    name: string;
}

const Container = styled.div`
    padding: 8px;
    display: flex;
    justify-content: flex-end;
`
export const Main = () => {
    const { account, chainId } = useEthers();
    const network = chainId ? helper[chainId] : "dev";
    console.log(chainId);
    console.log(network);
    const rewardTokenAddress = chainId ?
        networkMapping[String(chainId)]["RewardToken"][0] :
        constants.AddressZero;
    const tokenFarmAddress = chainId ?
        networkMapping[String(chainId)]["TokenFarm"][0] :
        constants.AddressZero;
    const wethTokenAddress = chainId ?
        brownieConfig["networks"][network]["weth_token"] :
        constants.AddressZero;
    const daiTokenAddress = chainId ?
        brownieConfig["networks"][network]["fau_token"] :
        constants.AddressZero;
    const ethUsdFeedAddress = chainId ?
        brownieConfig["networks"][network]["eth_usd_feed"] :
        constants.AddressZero;
    const daiUsdFeedAddress = chainId ?
        brownieConfig["networks"][network]["dai_usd_feed"] :
        constants.AddressZero;
    // console.log(rewardTokenAddress);
    // console.log(tokenFarmAddress);
    // console.log(wethTokenAddress);
    // console.log(daiTokenAddress);
    // console.log(ethUsdFeedAddress);
    // console.log(daiUsdFeedAddress);

    const supportedTokens: Array<Token> = [
        {
            image: rwd,
            address: rewardTokenAddress,
            name: "RWD"
        },
        {
            image: eth,
            address: wethTokenAddress,
            name: "WETH"
        },
        {
            image: dai,
            address: daiTokenAddress,
            name: "DAI"
        },
    ]

    return (
        <div>Hi</div>
    )
}