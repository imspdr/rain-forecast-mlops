import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useRootStore } from "@src/store/RootStoreProvider";
import { useEffect, useState } from "react";
import { Typography, Button } from "@mui/material";
import TrainTable from "@src/components/train/TrainTable";
import DetailPage from "@src/pages/DetailPage";
import DeleteDialog from "@src/components/train/DeleteDialog";
import CreateDialog from "@src/components/train/CreateDialog";
import { TrainedModel } from "@src/store/type";

function TrainPage() {
  const rootStore = useRootStore();
  const [createOpen, setCreateOpen] = useState(false);

  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleteId, setDeleteId] = useState(-1);
  const [deleteName, setDeleteName] = useState("");

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
              onClick={(name: string) => {
                rootStore.detail = name;
              }}
              onDelete={(id: number, name: string) => {
                setDeleteId(id);
                setDeleteName(name);
                setDeleteOpen(true);
              }}
            />
          </div>
        </div>
      )}

      {createOpen && (
        <CreateDialog open={createOpen} setOpen={setCreateOpen} onCreate={rootStore.createTrain} />
      )}
      {deleteOpen && (
        <DeleteDialog
          open={deleteOpen}
          setOpen={setDeleteOpen}
          name={deleteName}
          onDelete={() => {
            rootStore.deleteTrainedModel(deleteName);
            rootStore.deleteTrain(deleteId);
          }}
        />
      )}
    </>
  );
}

export default observer(TrainPage);
