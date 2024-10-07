import React from "react";
import { ResponsiveBar } from "@nivo/bar";

export default function HistogramChart({ data }) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <div style={{ height: "220px", width: "1100px" }}>
        <ResponsiveBar
          layout="vertical"
          margin={{ top: 20, right: 50, bottom: 50, left: 50 }}
          data={data.train}
          indexBy="x"
          keys={["y"]}
          colors={{ scheme: "category10" }}
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
          motionStiffness={170}
          motionDamping={26}
          labelSkipWidth={12}
          labelSkipHeight={12}
          borderWidth={1}
        />
      </div>
    </div>
  );
}
