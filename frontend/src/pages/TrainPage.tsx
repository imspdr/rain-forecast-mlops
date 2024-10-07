import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useRootStore } from "@src/store/RootStoreProvider";
import { Typography } from "@mui/material";
import TrainTable from "@src/components/train/TrainTable";

function TrainPage() {
  const rootStore = useRootStore();
  return (
    <div
      css={css`
        display: flex;
        width: 99vw;
        flex-direction: column;
        align-items: flex-start;
      `}
    >
      <Typography>TRAIN</Typography>
      <TrainTable trains={rootStore.trains} />
    </div>
  );
}

export default observer(TrainPage);
