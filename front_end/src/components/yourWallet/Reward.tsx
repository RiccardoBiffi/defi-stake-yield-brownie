import { Token } from "../Main";
import styled from "@emotion/styled";
import { useGetUserTVL } from "../../hooks/useGetUserTVL";
import { useEthers } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { ClickAwayListener, IconButton, Tooltip, tooltipClasses, TooltipProps } from "@mui/material";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";

const ContainerBackground = styled.div`
    margin: 8px 0;
    border-radius: 30px;
    background: linear-gradient(-23deg, hsl(237, 61%, 15%), hsl(188, 61%, 30%), hsl(136, 39%, 37%));
`
const Container = styled.div`
    padding: 4px!important;
    display: flex;
    align-items: center;
`
const RewardMsg = styled.div`
    background-color: white;
    border-radius: 25px;
    font-size: 28px;
    padding: 0 16px;
`
const Amount = styled.span`
    font-weight: 700;
    padding-right: 8px;
`
const TokenImg = styled.img`
    height: 32px;
    width: auto;
    position: relative;
    top: 4px;
`
const InfoTooltip = styled(Tooltip)`
    padding: 0;
    position: relative;
    top: -5px;
    right: -7px;
    background-color: red;
`
const Header = styled.h2`
    color: white;
`

const informationString = "You get 1 RWD for every USD of your TVL (Total Value Locked). You cannot withdraw them, the token issuance is decided by admins."

export interface RewardProps {
    token: Token | undefined;
}

export const Reward = ({ token }: RewardProps) => {
    const { account } = useEthers();
    const userTVL = useGetUserTVL(account);
    const formattedUserTVL: string =
        userTVL ?
            parseFloat(formatUnits(userTVL, 18)).toFixed(2) :
            "0";
    console.log(userTVL);

    return (
        <ContainerBackground>
            <Container>
                {
                    token ?
                        <RewardMsg>Your accrued RWD is <Amount>{formattedUserTVL}</Amount>
                            <TokenImg src={token.image} alt={token.name} />

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

                        </RewardMsg>

                        :
                        <Header>An error occured</Header>
                }
            </Container>
        </ContainerBackground>
    );
}