import { Token } from "../Main";
import { constants, Contract, utils } from "ethers"
import styled from "@emotion/styled";
import { useGetUserTVL } from "../../hooks/useGetUserTVL";
import { useEthers } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";


const TokenImg = styled.img`
    height: 32px;
    width: auto;
    position: relative;
    top: 4px;
`
const Container = styled.div`
    padding: 8px 0;
    display: flex;
    align-items: center;
`
const Amount = styled.span`
    font-weight: 700;
    padding-right: 8px;
`

const Header = styled.h2`
    color: white;
`
const RewardMsg = styled.div`
    background-color: white;
    border-radius: 25px;
    font-size: 30px;
    padding: 0 16px;
`

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
        <Container>
            {
                token ?
                    <RewardMsg>Your accrued RWD is <Amount>{formattedUserTVL}</Amount>
                        <TokenImg src={token.image} alt="asd" />
                    </RewardMsg>

                    :
                    <Header>An error occured</Header>
            }
        </Container>
    );
}