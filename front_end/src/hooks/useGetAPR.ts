import { Falsy, useCall, useEthers } from "@usedapp/core"
import { constants, Contract, utils } from "ethers";
import networkMapping from "../chain_info/deployments/map.json";
import TokenFarm from "../chain_info/contracts/TokenFarm.json";


export function useGetAPR(
) {
    const { chainId } = useEthers();
    const { abi: tf_abi } = TokenFarm;

    const tokenFarmAddr = chainId ?
        networkMapping[String(chainId)]["TokenFarm"][0] :
        constants.AddressZero;
    const tokenFarmInterface = new utils.Interface(tf_abi);

    const { value, error } =
        useCall(
            {
                contract: new Contract(tokenFarmAddr, tokenFarmInterface),
                method: 'APR',
                args: []
            }
        ) ?? {}
    if (error) {
        console.error(error.message);
        return 0;
    }
    return value?.[0]
}