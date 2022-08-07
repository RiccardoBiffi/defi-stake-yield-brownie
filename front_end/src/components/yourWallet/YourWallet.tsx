import { Box } from "@mui/material";
import { Token } from "../Main";

interface YourWalletProps {
    supportedTokens: Array<Token>
}

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
    return (
        <Box>
            <h1>Your wallet!</h1>
            <div>Wallet description</div>
        </Box>

    )
}