import styled from "@emotion/styled";
import { Token } from "./Main";

const Container = styled.div`
    display: inline-grid;
    grid-template-columns: auto auto auto;
    gap: 8px;
    align-items: center;
`

const TokenImg = styled.img`
    height: 30px;
    width: auto;
`

const Amount = styled.h2`
    font-weight: 700;
`

export interface BalanceMsgProps {
    label: string;
    token: Token;
    amount: number;
}

export const BalanceMsg = ({ label, token, amount }: BalanceMsgProps) => {
    return (
        <Container>
            <h2>{label}</h2>
            <Amount>{amount}</Amount>
            <TokenImg src={token.image} alt={token.name} />
        </Container>
    )
}