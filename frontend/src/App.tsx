import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useState } from "react";
import { Tabs, Tab, Divider } from "@mui/material";
import TrainPage from "./pages/TrainPage";
import InferPage from "./pages/InferPage";

function App() {
  const [tab, setTab] = useState(1);

  const tabInfos = [
    {
      value: 0,
      name: "학습",
    },
    {
      value: 1,
      name: "추론",
    },
  ];

  return (
    <div
      css={css`
        display: flex;
        flex-direction: column;
        padding: 20px;
      `}
    >
      <Tabs value={tab} onChange={(e, v) => setTab(v)}>
        {tabInfos.map((tabinfo) => (
          <Tab
            css={css`
              width: 140px;
              font-size: 20px;
            `}
            value={tabinfo.value}
            label={tabinfo.name}
          />
        ))}
      </Tabs>
      <Divider
        css={css`
          width: 100%;
          color: #d6d6d6;
        `}
      />
      <div
        css={css`
          display: flex;
          flex-direction: row;
          justify-content: center;
        `}
      >
        {(function test(v: number) {
          switch (v) {
            case 0:
              return <TrainPage />;
            case 1:
              return <InferPage />;
            default:
              return <TrainPage />;
          }
        })(tab)}
      </div>
    </div>
  );
}

export default observer(App);
