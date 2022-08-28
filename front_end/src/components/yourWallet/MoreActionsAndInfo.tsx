import { Token } from "../Main";
import { useEthers } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { BalanceMsg } from "../BalanceMsg"
import { useTokenStakerAmount } from "../../hooks/useTokenStakerAmount"
import { formatBigNumber } from "../../utils";


export interface MoreActionsAndInfoProps {
    token: Token;
}

export const MoreActionsAndInfo = ({ token }: MoreActionsAndInfoProps) => {
    const { image, address: token_addr, name } = token;
    const { account } = useEthers();
    const tokenBalance = useTokenStakerAmount(token_addr, account)?.toString()
    const balanceFormatted = formatBigNumber(tokenBalance, 18, 4)

    return (
        <>
            Add to metamask
        </>
    )
}