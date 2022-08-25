import { Token } from "../Main";
import { useEthers, useTokenBalance } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { BalanceMsg } from "../BalanceMsg"


export interface WalletBalanceProps {
    token: Token;
}

export const WalletBalance = ({ token }: WalletBalanceProps) => {
    const { image, address: token_addr, name } = token;
    const { account } = useEthers();
    const tokenBalance = useTokenBalance(token_addr, account)?.toString()
    const formattedTokenBalance: number =
        tokenBalance ?
            parseFloat(formatUnits(tokenBalance, 18)) :
            0;
    return (
        <BalanceMsg
            label={`Your ${name} balance is`}
            token={token}
            amount={formattedTokenBalance} />
    )
}