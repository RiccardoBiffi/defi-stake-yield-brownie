import { Token } from "../Main";
import { useEthers, useTokenBalance } from "@usedapp/core";
import { BalanceMsg } from "../BalanceMsg";
import { formatBigNumber } from "../../utils";

export interface WalletBalanceProps {
  token: Token;
}

export const WalletBalance = ({ token }: WalletBalanceProps) => {
  const { address: token_addr, name } = token;
  const { account } = useEthers();
  const tokenBalance = useTokenBalance(token_addr, account)?.toString();
  const balanceFormatted = formatBigNumber(tokenBalance, 18, 4);
  return (
    <BalanceMsg
      label={`Your ${name} balance is`}
      token={token}
      amount={balanceFormatted}
    />
  );
};
