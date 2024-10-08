import { Card } from "@mui/material";
import { css } from "@emotion/react";
import { Typography } from "@mui/material";
import { Base, CategoricalDist } from "@src/store/type";
import { ResponsiveBar } from "@nivo/bar";

export default function CategoricalChart(props: {
  width: number;
  height: number;
  dist: CategoricalDist;
}) {
  return (
    <div
      css={css`
        position: relative;
        width: ${props.width}px;
        height: ${props.height}px;
      `}
    >
      <ResponsiveBar
        layout="vertical"
        margin={{ top: 20, right: 30, bottom: 40, left: 30 }}
        data={props.dist.value_percentage
          .sort((a, b) => b.value - a.value)
          .filter((_, i) => i < 15)
          .map((item: Base) => {
            return {
              name: item.name,
              value: Number(item.value.toFixed(2)),
            };
          })}
        indexBy="name"
        keys={["value"]}
        colors={"#87CEEB"}
        borderColor={{
          from: "color",
          modifiers: [["darker", 2.6]],
        }}
        enableGridY={false}
        enableGridX={false}
        axisLeft={null}
        padding={0}
        labelTextColor={{
          from: "color",
          modifiers: [["darker", 1.4]],
        }}
        isInteractive={true}
        label={(d) => `${d.value}%`}
        labelSkipWidth={12}
        labelSkipHeight={12}
        borderWidth={1}
      />
    </div>
  );
}
