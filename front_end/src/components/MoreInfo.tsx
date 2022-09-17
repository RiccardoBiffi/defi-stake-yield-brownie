import { useEthers } from "@usedapp/core";

export const MoreInfo = () => {
    const { account } = useEthers();

    return (
        <>
            More info
        </>
    )
}