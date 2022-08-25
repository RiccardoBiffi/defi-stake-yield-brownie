import { Token } from "../Main";
import { useEthers } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { BalanceMsg } from "../BalanceMsg"
import { useTokenStakerAmount } from "../../hooks/useTokenStakerAmount"
import { formatBigNumber } from "../../utils";


export interface StakeBalanceProps {
    token: Token;
}

export const StakeBalance = ({ token }: StakeBalanceProps) => {
    const { image, address: token_addr, name } = token;
    const { account } = useEthers();
    const tokenBalance = useTokenStakerAmount(token_addr, account)?.toString()
    const balanceFormatted = formatBigNumber(tokenBalance, 18, 4)

    return (
        <BalanceMsg
            label={`Your staked ${name} balance is`}
            token={token}
            amount={balanceFormatted} />
    )
}