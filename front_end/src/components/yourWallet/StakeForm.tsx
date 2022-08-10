import { Token } from "../Main";
import { useEthers, useTokenBalance, useNotifications, Notification } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { Alert, Button, CircularProgress, Input, Snackbar } from "@mui/material";
import React, { useEffect, useState } from "react";
import { useStakeTokens } from "../../hooks/useStakeTokens";
import { utils } from "ethers";
import styled from "@emotion/styled";

const Stake = styled(Button)`
    margin-top: 16px;
    border: 1px solid #1976d2 !important;
    border-radius: 8px;
`

export interface StakeFormProps {
  token: Token;
}

function isTransactionSucceeded(notifications: Notification[], transactionName: string) {
  return notifications.filter(
    (notification) =>
      notification.type === "transactionSucceed" &&
      notification.transactionName === transactionName
  ).length > 0;
}

export const StakeForm = ({ token }: StakeFormProps) => {
  const { address: tokenAddr, name } = token;
  const { account } = useEthers();
  const tokenBalance = useTokenBalance(tokenAddr, account)?.toString()
  const formattedTokenBalance: number =
    tokenBalance ?
      parseFloat(formatUnits(tokenBalance, 18)) :
      0;

  const { notifications } = useNotifications();
  const [amount, setAmopunt] = useState<number | string | Array<number | string>>(0);
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newAmount = event.target.value === "" ? "" : Number(event.target.value);
    setAmopunt(newAmount);
  }

  const { approveAndStake, overallState } = useStakeTokens(tokenAddr);
  const handleStakeSubmit = () => {
    const amountWei = utils.parseEther(amount.toString()).toString();
    return approveAndStake(amountWei);
  }

  const isValidating = overallState.status === "Mining";
  const [showERC20ApprovalSuccess, setShowERC20ApprovalSuccess] = useState<boolean>(false);
  const [showStakeTokenSuccess, setShowStakeTokenSuccess] = useState<boolean>(false);

  const handleCloseERC20ApprovalSnackbar = () => {
    setShowERC20ApprovalSuccess(false);
  }

  const handleCloseStakeSnackbar = () => {
    setShowStakeTokenSuccess(false);
  }

  useEffect(() => {
    if (isTransactionSucceeded(notifications, "Approve ERC20 transfer")) {
      setShowERC20ApprovalSuccess(true);
      setShowStakeTokenSuccess(false);
    }

    if (isTransactionSucceeded(notifications, "Stake tokens")) {
      setShowStakeTokenSuccess(true);
      setShowERC20ApprovalSuccess(false);
    }
  }, [notifications, showERC20ApprovalSuccess, showStakeTokenSuccess]);

  return (
    <>
      <Input onChange={handleInputChange} />

      <Stake
        onClick={handleStakeSubmit}
        color="primary"
        size="large"
        disabled={isValidating}>
        {isValidating ?
          <CircularProgress size={26} />
          :
          "Stake!!!"}
      </Stake>

      <Snackbar
        open={showERC20ApprovalSuccess}
        autoHideDuration={5000}
        onClose={handleCloseERC20ApprovalSnackbar}
      >
        <Alert
          onClose={handleCloseERC20ApprovalSnackbar}
          severity="success"
        >
          ERC20 token transfer approved! <br />
          Now approve the next transaction to stake.
        </Alert>
      </Snackbar>

      <Snackbar
        open={showStakeTokenSuccess}
        autoHideDuration={5000}
        onClose={handleCloseStakeSnackbar}
      >
        <Alert
          onClose={handleCloseStakeSnackbar}
          severity="success"
        >
          Token staked succesfully!
        </Alert>
      </Snackbar>

    </>
  )
}