import { Falsy, useCall, useEthers } from "@usedapp/core"
import { constants, Contract, utils } from "ethers";
import networkMapping from "../chain_info/deployments/map.json";
import TokenFarm from "../chain_info/contracts/TokenFarm.json";


export function useGetUserTVL(
    userAddress: string | Falsy,
) {
    const { chainId } = useEthers();
    const { abi: tf_abi } = TokenFarm;

    const tokenFarmAddr = chainId ?
        networkMapping[String(chainId)]["TokenFarm"][0] :
        constants.AddressZero;
    const tokenFarmInterface = new utils.Interface(tf_abi);

    const { value, error } =
        useCall(
            userAddress && {
                contract: new Contract(tokenFarmAddr, tokenFarmInterface),
                method: 'getUserTVL',
                args: [userAddress],
            }
        ) ?? {}
    if (error) {
        console.error(error.message)
        return undefined
    }
    return value?.[0]
}