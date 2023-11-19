import { useEthers, useContractFunction } from "@usedapp/core";
import TokenFarm from "../chain_info/contracts/TokenFarm.json";
import ERC20 from "../chain_info/contracts/dependencies/OpenZeppelin/openzeppelin-contracts@4.7.1/ERC20.json";
import networkMapping from "../chain_info/deployments/map.json";
import { constants, Contract, utils } from "ethers";


export const useUnstakeTokens = (tokenAddress: string) => {
    const { chainId } = useEthers();
    const { abi: tf_abi } = TokenFarm;
    const { abi: erc20_abi } = ERC20;

    const tokenFarmAddr = chainId ?
        networkMapping[String(chainId)]["TokenFarm"][0] :
        constants.AddressZero;
    const tokenFarmInterface = new utils.Interface(tf_abi);
    const tokenFarm = new Contract(tokenFarmAddr, tokenFarmInterface);

    // const erc20Interface = new utils.Interface(erc20_abi);
    // const erc20 = new Contract(tokenAddress, erc20Interface);

    //unstake
    const { send: unstakeSend, state: unstakeState } =
        useContractFunction(tokenFarm, "unstakeTokenAndWithdrawMyReward", { transactionName: "Unstake tokens" });

    return { unstakeSend, unstakeState }
}