import styled from "@emotion/styled";

const Container = styled.div`
    display: inline-grid;
    grid-template-columns: auto auto auto;
    gap: 8px;
    align-items: center;
`

const TokenImg = styled.img`
    height: 32px;
    width: auto;
`

const Amount = styled.h2`
    font-weight: 700;
`

export interface BalanceMsgProps {
    label: string;
    tokenImgSrc: string;
    amount: number;
}

export const BalanceMsg = ({ label, tokenImgSrc, amount }: BalanceMsgProps) => {
    return (
        <Container>
            <h2>{label}</h2>
            <Amount>{amount}</Amount>
            <TokenImg src={tokenImgSrc} alt="asd" />
        </Container>
    )
}