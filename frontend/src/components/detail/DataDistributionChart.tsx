import { Card } from "@mui/material";
import { css } from "@emotion/react";
import { Typography } from "@mui/material";
import { Base, DataDistribution } from "@src/store/type";

export default function DataDistributionChart(props: {
  width: number;
  height: number;
  dataDistribution: DataDistribution | undefined;
}) {
  return (
    <Card
      css={css`
        width: ${props.width}px;
        height: ${props.height}px;
        border-radius: 20px;
        padding: 20px;

        display: flex;
        flex-direction: column;
        gap: 20px;
      `}
      elevation={0}
    >
      <Typography>{"데이터 분포"}</Typography>
    </Card>
  );
}
