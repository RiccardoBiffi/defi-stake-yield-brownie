import styled from "@emotion/styled";

const Container = styled.div`
    display: inline-grid;
    grid-template-columns: auto auto auto;
    gap: 16px;
    align-items: center;
`

const TokenImg = styled.img`
    height: 32px;
    width: auto;
`

const Amount = styled.p`
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
            <TokenImg src={tokenImgSrc} alt="asd" />
            <Amount>{amount}</Amount>
        </Container>
    )
}