import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useRootStore } from "@src/store/RootStoreProvider";
import { useEffect, useState } from "react";
import { Button, Typography } from "@mui/material";
import TrainedModelList from "@src/components/infer/TrainedModelList";
import { DateText } from "@src/components/train/CreateDialog";
import InferResult from "@src/components/infer/InferResult";
import { properDate } from "@src/store/util";

function generateDate() {
  const now = new Date();

  const year = String(now.getFullYear());
  const month = String(now.getMonth() + 1).padStart(2, "0"); // Ensure 2 digits
  const day = String(now.getDate()).padStart(2, "0"); // Ensure 2 digits

  const formattedDateTime = `${year}${month}${day}`;
  return formattedDateTime;
}

function InferPage() {
  const rootStore = useRootStore();
  const [nowModel, setNowModel] = useState("");
  const [selectedDate, setSelectedDate] = useState(generateDate());
  const [result, setResult] = useState<{
    y_hat: number[];
    y_true: number[];
    y_proba: number[];
  }>({
    y_hat: [],
    y_true: [],
    y_proba: [],
  });
  const refresh = () => {
    rootStore.getDeployedTrainedModels();
  };
  const infer = async () => {
    if (properDate(selectedDate) && !!nowModel) {
      rootStore.infer(selectedDate, nowModel).then((data) => {
        setResult(data.predictions[0]!);
      });
    }
  };
  useEffect(() => {
    rootStore.getDeployedTrainedModels();
  }, []);
  return (
    <div
      css={css`
        display: flex;
        flex-direction: row;
        gap: 30px;
      `}
    >
      <div
        css={css`
          display: flex;
          flex-direction: column;
        `}
      >
        <Button
          css={css`
            height: 40px;
            width: 120px;
            font-size: 15px;
            margin: 20px 10px;
          `}
          variant={"outlined"}
          onClick={refresh}
        >
          새로고침
        </Button>
        <TrainedModelList
          deployTrainedModels={rootStore.deployedModels}
          onClick={(name: string) => {
            setNowModel(name);
          }}
        />
      </div>
      <div
        css={css`
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 20px;
          gap: 10px;
        `}
      >
        <div
          css={css`
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            gap: 10px;
            height: 80px;
          `}
        >
          <div
            css={css`
              width: 280px;
              height: 60px;
              display: flex;
              flex-direction: row;
              align-items: center;
            `}
          >
            <Typography>{`선택된 모델 : ${nowModel}`}</Typography>
          </div>
          <DateText day={selectedDate} setDay={setSelectedDate} label={"추론할 날짜"} />
          <Button
            css={css`
              height: 56px;
              width: 120px;
              font-size: 25px;
            `}
            variant={"outlined"}
            onClick={infer}
          >
            추론
          </Button>
        </div>
        <InferResult yHat={result.y_hat} yTrue={result.y_true} yProba={result.y_proba} />
      </div>
    </div>
  );
}

export default observer(InferPage);
