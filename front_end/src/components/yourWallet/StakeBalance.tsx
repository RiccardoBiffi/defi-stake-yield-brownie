import { Token } from "../Main";
import { useEthers, useTokenBalance } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { BalanceMsg } from "../BalanceMsg"
import { useTokenStakerAmount } from "../../hooks/useTokenStakerAmount"


export interface StakeBalanceProps {
    token: Token;
}

export const StakeBalance = ({ token }: StakeBalanceProps) => {
    const { image, address: token_addr, name } = token;
    const { account } = useEthers();
    const tokenBalance = useTokenStakerAmount(token_addr, account)?.toString()
    const formattedTokenBalance: number =
        tokenBalance ?
            parseFloat(formatUnits(tokenBalance, 18)) :
            0;
    return (
        <BalanceMsg
            label={`Your staked ${name} balance is`}
            tokenImgSrc={image}
            amount={formattedTokenBalance} />
    )
}