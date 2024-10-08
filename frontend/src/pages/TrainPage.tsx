import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useRootStore } from "@src/store/RootStoreProvider";
import { useEffect, useState } from "react";
import { Typography, Button } from "@mui/material";
import TrainTable from "@src/components/train/TrainTable";
import DetailMain from "@src/components/detail/DetailMain";
import DeleteDialog from "@src/components/train/DeleteDialog";
import CreateDialog from "@src/components/train/CreateDialog";
import { TrainedModel } from "@src/store/type";

function TrainPage() {
  const rootStore = useRootStore();
  const [createOpen, setCreateOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [detail, setDetail] = useState("");

  useEffect(() => {
    rootStore.getTrains();
    setInterval(() => {
      rootStore.getTrains();
      rootStore.getTrainedModels();
    }, 20000);
  }, []);
  return (
    <>
      {detail ? (
        <DetailMain trainedModel={rootStore.trainedModels.find((tm) => tm.train_name === detail)} />
      ) : (
        <div
          css={css`
            display: flex;
            width: 99vw;
            flex-direction: column;
            align-items: center;
          `}
        >
          <div
            css={css`
              display: flex;
              flex-direction: column;
              align-items: flex-start;
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
              onClick={() => setCreateOpen(true)}
            >
              새 학습 생성
            </Button>
            <TrainTable
              trains={rootStore.trains}
              onClick={(name: string) => {
                setDetail(name);
              }}
            />
          </div>
        </div>
      )}

      <CreateDialog open={createOpen} setOpen={setCreateOpen} onCreate={rootStore.createTrain} />
    </>
  );
}

export default observer(TrainPage);
