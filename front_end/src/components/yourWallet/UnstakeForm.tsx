import { Token } from "../Main";
import { useNotifications, Notification } from "@usedapp/core";
import { Alert, Button, CircularProgress, Input, Snackbar } from "@mui/material";
import { useEffect, useState } from "react";
import { useUnstakeTokens } from "../../hooks/useUnstakeTokens";
import styled from "@emotion/styled";

const StakeButton = styled(Button)`
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

export const UnstakeForm = ({ token }: StakeFormProps) => {
    const { address: tokenAddr, name } = token;

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
        else {
            setShowUnstakeTokenSuccess(false);
        }
    }, [notifications, showUnstakeTokenSuccess]);

    return (
        <>
            <StakeButton
                onClick={handleUnstakeSubmit}
                color="primary"
                size="large"
                disabled={isValidating}>
                {isValidating ?
                    <CircularProgress size={26} />
                    :
                    "Unstake!!!"}
            </StakeButton>

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