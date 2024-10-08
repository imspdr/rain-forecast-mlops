import { css } from "@emotion/react";
import { List, ListItem, ListItemButton, ListItemText, Divider, Card } from "@mui/material";
import { Train } from "@src/store/type";

function TrainRow(props: { train: Train; onClick: (name: string) => void }) {
  return (
    <ListItemButton onClick={() => props.onClick(props.train.name)}>
      <ListItemText
        css={css`
          width: 180px;
        `}
        primary={props.train.name}
      />
      <ListItemText
        css={css`
          width: 200px;
        `}
        primary={`${props.train.start_day} ~ ${props.train.end_day}`}
      />
      <ListItemText
        css={css`
          width: 200px;
        `}
        primary={props.train.created_at}
      />
      <ListItemText
        css={css`
          width: 200px;
        `}
        primary={props.train.finished_at ? props.train.finished_at : "-"}
      />
      <ListItemText
        css={css`
          width: 120px;
        `}
        primary={props.train.status}
      />
    </ListItemButton>
  );
}

export default function TrainTable(props: { trains: Train[]; onClick: (name: string) => void }) {
  return (
    <Card elevation={1}>
      <List>
        <ListItem>
          <ListItemText
            css={css`
              width: 180px;
            `}
            primary={"학습명"}
          />
          <ListItemText
            css={css`
              width: 200px;
            `}
            primary={`학습 데이터 범위`}
          />
          <ListItemText
            css={css`
              width: 200px;
            `}
            primary={"생성 시간"}
          />
          <ListItemText
            css={css`
              width: 200px;
            `}
            primary={"종료 시간"}
          />
          <ListItemText
            css={css`
              width: 120px;
            `}
            primary={"상태"}
          />
        </ListItem>
        {props.trains.map((train: Train) => (
          <>
            <Divider />
            <TrainRow train={train} onClick={props.onClick} />
          </>
        ))}

        <Divider />
      </List>
    </Card>
  );
}
