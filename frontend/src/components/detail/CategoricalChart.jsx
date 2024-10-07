import React from "react";
import { ResponsiveBar } from "@nivo/bar";

export default function CategoricalChart({ data, keys }) {
  return (
    <ResponsiveBar
      layout="vertical"
      margin={{ top: 50, right: 140, bottom: 50, left: 50 }}
      data={data}
      indexBy="index"
      minValue={0}
      maxValue={100}
      keys={keys}
      colors={{ scheme: "blues" }}
      borderColor={{ from: "color", modifiers: [["darker", 2.6]] }}
      enableGridY={false}
      enableGridX={false}
      axisLeft={null}
      padding={0.3}
      labelTextColor={{ from: "color", modifiers: [["darker", 1.4]] }}
      isInteractive={true}
      motionStiffness={170}
      motionDamping={26}
      label={(d) => `${d.value.toFixed(1)}%`}
      labelSkipWidth={12}
      labelSkipHeight={12}
      borderWidth={1}
      legends={[
        {
          dataFrom: "keys",
          anchor: "bottom-right",
          direction: "column",
          justify: false,
          translateX: 100,
          translateY: 0,
          itemsSpacing: 0,
          itemDirection: "left-to-right",
          itemWidth: 80,
          itemHeight: 20,
          itemOpacity: 1,
          symbolSize: 12,
          symbolShape: "circle",
        },
      ]}
    />
  );
}
