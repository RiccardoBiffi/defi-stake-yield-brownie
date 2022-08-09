import { Token } from "../Main";
import { useEthers, useTokenBalance } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { Button, Input } from "@mui/material";
import React, { useState } from "react";
import { useStakeTokens } from "../../hooks/useStakeTokens";
import { utils } from "ethers";


export interface StakeFormProps {
    token: Token;
}

export const StakeForm = ({ token }: StakeFormProps) => {
    const { address: tokenAddr, name } = token;
    const { account } = useEthers();
    const tokenBalance = useTokenBalance(tokenAddr, account)?.toString()
    const formattedTokenBalance: number =
        tokenBalance ?
            parseFloat(formatUnits(tokenBalance, 18)) :
            0;

    const [amount, setAmopunt] = useState<number | string | Array<number | string>>(0);
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newAmount = event.target.value === "" ? "" : Number(event.target.value);
        setAmopunt(newAmount);
    }

    const { approve, approveErc20State } = useStakeTokens(tokenAddr);
    const handleStakeSubmit = () => {
        const amountWei = utils.parseEther(amount.toString()).toString();
        return approve(amountWei);
    }


    return (
        <div>
            <Input onChange={handleInputChange} />
            <Button
                onClick={handleStakeSubmit}
                color="primary"
                size="large">
                STAKE!
            </Button>
        </div>
    )
}