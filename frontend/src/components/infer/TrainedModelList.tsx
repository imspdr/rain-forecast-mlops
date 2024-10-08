import { css } from "@emotion/react";
import { List, ListItem, ListItemText, Divider, Card, ListItemButton } from "@mui/material";
import { TrainedModelSimple } from "@src/store/type";

export default function TrainedModelList(props: {
  deployTrainedModels: TrainedModelSimple[];
  onClick: (name: string) => void;
}) {
  return (
    <Card
      elevation={0}
      css={css`
        width: 250px;
        height: 520px;
        overflow: auto;
      `}
    >
      <List>
        <ListItem>
          <ListItemText primary={"학습명"} />
        </ListItem>
        <Divider />
        {props.deployTrainedModels.map((tms: TrainedModelSimple) => (
          <>
            <ListItemButton
              onClick={() => props.onClick(tms.train_name)}
              css={css`
                height: 50px;
                padding: 10px 20px;
              `}
            >
              <ListItemText>{tms.train_name}</ListItemText>
            </ListItemButton>
            <Divider />
          </>
        ))}
        {props.deployTrainedModels.length === 0 && (
          <div
            css={css`
              height: 400px;
              width: 250px;
              display: flex;
              justify-content: center;
              align-items: center;
            `}
          >
            배포된 모델이 없습니다
          </div>
        )}
      </List>
    </Card>
  );
}
