import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useRootStore } from "@src/store/RootStoreProvider";
import { DataDistribution, TrainedModelInfo } from "@src/store/type";
import { useState, useEffect } from "react";
import { ArrowBackIos } from "@mui/icons-material";
import { Card, Button, Typography } from "@mui/material";
import FeatureImportance from "@src/components/detail/FeatureImportance";
import ModelTitle from "@src/components/detail/ModelTitle";
import DataDistributionChart from "@src/components/detail/DataDistributionChart";
import Evaluate from "@src/components/detail/Evaluate";

function DetailPage() {
  const rootStore = useRootStore();
  const [dataDistribution, setDataDistribution] = useState<DataDistribution[] | undefined>(
    undefined
  );
  const [trainedModelInfo, setTrainedModelInfo] = useState<TrainedModelInfo | undefined>(undefined);
  useEffect(() => {
    rootStore.detail &&
      rootStore
        .getTrainedModel(rootStore.detail?.name)
        .then((data) => {
          if (data) {
            setTrainedModelInfo(JSON.parse(data?.trained_model_info));
            setDataDistribution(JSON.parse(data?.data_distribution));
          }
        })
        .catch((e) => (rootStore.detail = undefined));
  }, [rootStore.detail]);

  const buttonCss = `
    color: #000000;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #ffffff;
  `;
  return (
    <div
      css={css`
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 30px;
        padding: 20px;
      `}
    >
      <div
        css={css`
          display: flex;
          flex-direction: row;
          gap: 30px;
        `}
      >
        <Button
          css={css`
            width: 80px;
            height: 240px;
            ${buttonCss}
          `}
          onClick={() => {
            rootStore.detail = undefined;
          }}
        >
          <ArrowBackIos />
        </Button>
        <ModelTitle
          trainName={rootStore.detail ? rootStore.detail.name : ""}
          config={trainedModelInfo?.best_config}
          width={500}
          height={200}
        />
        <Evaluate evaluate={trainedModelInfo?.evaluate} width={250} height={200} />

        <div
          css={css`
            display: flex;
            flex-direction: column;
            gap: 30px;
          `}
        >
          <Button
            css={css`
              width: 240px;
              height: 105px;
              ${buttonCss}
            `}
            onClick={() => {}}
          >
            <Typography variant="h5">배포하기</Typography>
          </Button>
          <Button
            css={css`
              width: 240px;
              height: 105px;
              ${buttonCss}
            `}
            onClick={() => {
              if (rootStore.detail) {
                rootStore.delete = {
                  id: rootStore.detail.id,
                  name: rootStore.detail.name,
                  open: true,
                };
              }
            }}
          >
            <Typography variant="h5">삭제하기</Typography>
          </Button>
        </div>
      </div>
      <div
        css={css`
          display: flex;
          flex-direction: row;
          gap: 30px;
        `}
      >
        <DataDistributionChart width={610} height={400} dataDistribution={dataDistribution} />
        <FeatureImportance data={trainedModelInfo?.feature_importance} width={520} height={400} />
      </div>
    </div>
  );
}

export default observer(DetailPage);
