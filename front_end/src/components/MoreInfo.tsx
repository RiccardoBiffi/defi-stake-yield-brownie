import { Token } from "../Main";
import { useEthers } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { BalanceMsg } from "../BalanceMsg"
import { useTokenStakerAmount } from "../../hooks/useTokenStakerAmount"
import { formatBigNumber } from "../../utils";



export const MoreInfo = () => {
    const { account } = useEthers();

    return (
        <>
            More info
        </>
    )
}