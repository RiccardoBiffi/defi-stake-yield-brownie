import { useEthers, useContractFunction } from "@usedapp/core";
import TokenFarm from "../chain_info/contracts/TokenFarm.json";
import ERC20 from "../chain_info/contracts/dependencies/OpenZeppelin/openzeppelin-contracts@4.7.1/ERC20.json";
import networkMapping from "../chain_info/deployments/map.json";
import { constants, Contract, utils } from "ethers";
import { useEffect, useState } from "react";

export const useStakeTokens = (tokenAddress: string) => {
    const { chainId } = useEthers();
    const { abi: tf_abi } = TokenFarm;
    const { abi: erc20_abi } = ERC20;

    const tokenFarmAddr = chainId ?
        networkMapping[String(chainId)]["TokenFarm"][0] :
        constants.AddressZero;
    const tokenFarmInterface = new utils.Interface(tf_abi);
    const tokenFarm = new Contract(tokenFarmAddr, tokenFarmInterface);

    const erc20Interface = new utils.Interface(erc20_abi);
    const erc20 = new Contract(tokenAddress, erc20Interface);

    //approve
    const { send: approveErc20Send, state: approveAndStakeErc20State } =
        useContractFunction(erc20, "approve", { transactionName: "Approve ERC20 transfer" });
    const approveAndStake = (amount: string) => {
        setAmountToStake(amount);
        return approveErc20Send(tokenFarmAddr, amount);
    }

    //stake
    const { send: stakeSend, state: stakeState } =
        useContractFunction(tokenFarm, "stakeTokens", { transactionName: "Stake tokens" });
    const [amountToStake, setAmountToStake] = useState<string>("0"); // default is 0

    // take a function and a list of vars to check and, when the vars the list change,
    // useEffect fires the function
    useEffect(() => {
        if (approveAndStakeErc20State.status === "Success") {
            stakeSend(amountToStake, tokenAddress);
        }
    }, [approveAndStakeErc20State, amountToStake, tokenAddress, stakeSend])

    const [overallState, setOverallState] = useState(approveAndStakeErc20State);

    useEffect(() => {
        if (approveAndStakeErc20State.status === "Success") {
            setOverallState(stakeState);
        }
        else {
            setOverallState(approveAndStakeErc20State);
        }
    }, [approveAndStakeErc20State, stakeState])

    return { approveAndStake, overallState }
}