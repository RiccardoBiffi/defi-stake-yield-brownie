import { Token } from "../Main";
import styled from "@emotion/styled";
import { useGetUserAccruedReward } from "../../hooks/useGetUserAccruedReward";
import { useEthers } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { IconButton, Tooltip } from "@mui/material";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import { useGetUserTVL } from "../../hooks/useGetUserTVL";
import { BigNumberish } from "ethers";
import { useGetAPR } from "../../hooks/useGetAPR";
import { formatBigNumber } from "../../utils";

const ContainerBackground = styled.div`
    width: 100%;
    padding: 4px;
    margin: 16px 0;
    border-radius: 30px;
    background: linear-gradient(-23deg, hsl(237, 61%, 15%), hsl(188, 61%, 30%), hsl(136, 39%, 37%));
    box-shadow: 0px 2px 9px 0px #00000088;
`
const Container = styled.div`
    background-color: white;
    border-radius: 25px;
    padding: 8px;
    display: flex;
`
const Section = styled.div`
    width: 100%;
    flex-direction: column;
    align-items: center;
    display: inline-flex;
    flex: 1 1 0px;
    font-size: 28px;
    padding: 0 16px;
`
const VerticalLine = styled.div`
    width: 4px;
    background: linear-gradient(135deg, hsl(237, 61%, 15%), hsl(188, 61%, 30%), hsl(136, 39%, 37%));
    border-radius: 10px;
`
const Message = styled.div`
    font-size: 20px;
    padding: 0 16px;
`
const Amount = styled.span`
    font-weight: 700;
`
const TokenImg = styled.img`
    height: 30px;
    width: auto;
    position: relative;
    top: 4px;
`
const InfoTooltip = styled(Tooltip)`
    padding: 0;
    position: relative;
    top: -2px;
    right: -5px;
`
const Header = styled.h2`
    color: white;
`

export interface RewardProps {
  token: Token | undefined;
}

export const Reward = ({ token }: RewardProps) => {
  const { account } = useEthers();
  const myTVL = useGetUserTVL(account);
  const apr = useGetAPR();
  const myReward = useGetUserAccruedReward(account);

  const myTVLFormatted = formatBigNumber(myTVL, 18);
  const myAPRFormatted = formatBigNumber(apr, 2);
  const myRewardFormatted = formatBigNumber(myReward, 18, 6);

  const informationString = `Enjoy ${myAPRFormatted}% APR on your TVL!`;


  return (
    <ContainerBackground>
      <Container>
        <Section>
          <Message>Your TVL</Message>
          <Amount>{myTVLFormatted} $</Amount>
        </Section>
        <VerticalLine />
        <Section>
          <Message>
            APR
          </Message>
          <Amount>
            {myAPRFormatted}%
          </Amount>
        </Section>
        <VerticalLine />
        <Section>
          {
            token ?
              <>
                <Message>
                  Your RWD
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
                </Message>
                <div>
                  <Amount>{myRewardFormatted} </Amount>
                  <TokenImg src={token.image} alt={token.name} />
                </div>
              </>
              :
              <Header>An error occured</Header>
          }
        </Section>
      </Container>
    </ContainerBackground>
  );
}