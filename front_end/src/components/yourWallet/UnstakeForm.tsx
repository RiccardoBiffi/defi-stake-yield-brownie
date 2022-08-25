import { Token } from "../Main";
import { useNotifications, Notification, useEthers } from "@usedapp/core";
import { Alert, Button, CircularProgress, Tooltip, IconButton, Snackbar } from "@mui/material";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import { useEffect, useState } from "react";
import { useUnstakeTokens } from "../../hooks/useUnstakeTokens";
import styled from "@emotion/styled";
import { useTokenStakerAmount } from "../../hooks/useTokenStakerAmount";
import { formatUnits } from "ethers/lib/utils";

const UnstakeButton = styled(Button)`
    margin-top: 16px;
    border: 2px solid #1976d2 !important;
    border-radius: 8px;
    font-weight: bold;
`
const InfoTooltip = styled(Tooltip)`
    padding: 0;
    position: relative;
    top: 8px;
    right: -7px;
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

const informationString = "When you unstake you automatically withdraw your accrued RWD"

export const UnstakeForm = ({ token }: StakeFormProps) => {
    const { account } = useEthers();
    const { address: tokenAddr } = token;
    const tokenBalance = useTokenStakerAmount(tokenAddr, account)?.toString()
    const formattedTokenBalance: number =
        tokenBalance ?
            parseFloat(formatUnits(tokenBalance, 18)) :
            0;

    const { notifications } = useNotifications();

    const { unstakeSend, unstakeState } = useUnstakeTokens(tokenAddr);
    const handleUnstakeSubmit = () => {
        return unstakeSend(token.address);
    }

    const isValidating = unstakeState.status === "Mining";
    const [showUnstakeTokenSuccess, setShowUnstakeTokenSuccess] = useState<boolean>(false);


    const handleCloseUnstakeSnackbar = () => {
        setShowUnstakeTokenSuccess(false);
    }

    useEffect(() => {
        if (isTransactionSucceeded(notifications, "Unstake tokens")) {
            setShowUnstakeTokenSuccess(true);
        }
    }, [notifications, showUnstakeTokenSuccess]);

    return (
        <>
            <div>
                <UnstakeButton
                    onClick={handleUnstakeSubmit}
                    color="primary"
                    size="large"
                    disabled={isValidating || formattedTokenBalance <= 0}>
                    {isValidating ?
                        <CircularProgress size={26} />
                        :
                        "Unstake"}
                </UnstakeButton>
                <InfoTooltip
                    title={informationString}
                    placement="right"
                    arrow
                >
                    <IconButton
                        size="small"
                        color="primary"
                    >
                        <InfoOutlinedIcon />
                    </IconButton>
                </InfoTooltip>
            </div>

            <Snackbar
                open={showUnstakeTokenSuccess}
                autoHideDuration={5000}
                onClose={handleCloseUnstakeSnackbar}
            >
                <Alert
                    onClose={handleCloseUnstakeSnackbar}
                    severity="success"
                >
                    Token unstaked succesfully!
                </Alert>
            </Snackbar>
        </>
    )
}