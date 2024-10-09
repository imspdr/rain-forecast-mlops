import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useRootStore } from "@src/store/RootStoreProvider";
import { useEffect, useState } from "react";
import { Typography, Button } from "@mui/material";
import TrainTable from "@src/components/train/TrainTable";
import DetailPage from "@src/pages/DetailPage";
import DeleteDialog from "@src/components/train/DeleteDialog";
import CreateDialog from "@src/components/train/CreateDialog";
import { Train } from "@src/store/type";

function TrainPage() {
  const rootStore = useRootStore();
  const [createOpen, setCreateOpen] = useState(false);

  const refresh = () => {
    rootStore.getTrains();
  };
  useEffect(() => {
    rootStore.getTrains();
  }, [rootStore.detail]);
  return (
    <>
      {!!rootStore.detail ? (
        <DetailPage />
      ) : (
        <div
          css={css`
            display: flex;
            flex-direction: column;
          `}
        >
          <div>
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
          </div>
          <TrainTable
            trains={rootStore.trains}
            onClick={(clicked: Train) => {
              if (clicked.status === "complete") {
                rootStore.detail = clicked;
              }
            }}
            onDelete={(id: number, name: string) => {
              rootStore.delete = {
                id: id,
                name: name,
                open: true,
              };
            }}
          />
        </div>
      )}

      {createOpen && (
        <CreateDialog open={createOpen} setOpen={setCreateOpen} onCreate={rootStore.createTrain} />
      )}
      {rootStore.delete.open && (
        <DeleteDialog
          open={rootStore.delete.open}
          setOpen={(v: boolean) => {
            rootStore.delete = {
              ...rootStore.delete,
              open: v,
            };
          }}
          name={rootStore.delete.name}
          onDelete={() => {
            rootStore.deleteTrain();
            rootStore.detail = undefined;
          }}
        />
      )}
    </>
  );
}

export default observer(TrainPage);
