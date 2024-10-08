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
import DeployDialog from "@src/components/train/DeployDialog";

function DetailPage() {
  const rootStore = useRootStore();
  const [dataDistribution, setDataDistribution] = useState<DataDistribution[] | undefined>(
    undefined
  );
  const [trainedModelInfo, setTrainedModelInfo] = useState<TrainedModelInfo | undefined>(undefined);
  const [isDeployed, setIsDeployed] = useState(false);
  const [deployOpen, setDeployOpen] = useState(false);
  const [trainedModelId, setTrainedModelId] = useState(-1);

  useEffect(() => {
    rootStore.detail &&
      rootStore
        .getTrainedModel(rootStore.detail?.name)
        .then((data) => {
          if (data) {
            setTrainedModelId(data?.id);
            setTrainedModelInfo(JSON.parse(data?.trained_model_info));
            setDataDistribution(JSON.parse(data?.data_distribution));
            setIsDeployed(data.deployed === "true");
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
        padding: 20px 20px 0px 20px;
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
            height: 200px;
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
          height={160}
        />
        <Evaluate evaluate={trainedModelInfo?.evaluate} width={280} height={160} />

        <div
          css={css`
            display: flex;
            flex-direction: column;
            gap: 30px;
          `}
        >
          <Button
            css={css`
              width: 210px;
              height: 85px;
              ${buttonCss}
            `}
            onClick={() => {
              setDeployOpen(true);
            }}
          >
            <Typography variant="h5">{isDeployed ? "배포 취소" : "배포하기"}</Typography>
          </Button>
          <Button
            css={css`
              width: 210px;
              height: 85px;
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
        <DataDistributionChart width={610} height={350} dataDistribution={dataDistribution} />
        <FeatureImportance data={trainedModelInfo?.feature_importance} width={520} height={350} />
      </div>
      {deployOpen && rootStore.detail && (
        <DeployDialog
          open={deployOpen}
          setOpen={setDeployOpen}
          isDeployed={isDeployed}
          name={rootStore.detail!.name}
          onDeploy={() => {
            isDeployed
              ? rootStore.undeployTrainedModel(trainedModelId).then(() => {
                  setIsDeployed(false);
                })
              : rootStore.deployTrainedModel(trainedModelId).then(() => {
                  setIsDeployed(true);
                });
          }}
        />
      )}
    </div>
  );
}

export default observer(DetailPage);
