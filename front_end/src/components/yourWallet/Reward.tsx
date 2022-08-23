import { Token } from "../Main";
import { constants, Contract, utils } from "ethers"
import styled from "@emotion/styled";
import { useGetUserTVL } from "../../hooks/useGetUserTVL";
import { useEthers } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";

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
    font-size: 30px;
    padding: 0 16px;
`
const TokenImg = styled.img`
    height: 32px;
    width: auto;
    position: relative;
    top: 4px;
`
const Amount = styled.span`
    font-weight: 700;
    padding-right: 8px;
`
const Header = styled.h2`
    color: white;
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
        <ContainerBackground>
            <Container>
                {
                    token ?
                        <RewardMsg>Your accrued RWD is <Amount>{formattedUserTVL}</Amount>
                            <TokenImg src={token.image} alt={token.name} />

                        </RewardMsg>

                        :
                        <Header>An error occured</Header>
                }
            </Container>
        </ContainerBackground>
    );
}