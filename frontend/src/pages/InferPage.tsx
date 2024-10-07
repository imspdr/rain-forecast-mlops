import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { useRootStore } from "@src/store/RootStoreProvider";

function InferPage() {
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
      INFER
    </div>
  );
}

export default observer(InferPage);
