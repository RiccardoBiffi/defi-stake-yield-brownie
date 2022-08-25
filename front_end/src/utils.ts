import { BigNumberish } from "ethers";
import { formatUnits } from "ethers/lib/utils";

export function formatBigNumber(number: BigNumberish | undefined, decimals: number, show = 2): string {
    return number ? parseFloat(formatUnits(number, decimals)).toFixed(show) : "0";
}