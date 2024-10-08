import { css } from "@emotion/react";
import { List, ListItem, ListItemButton, ListItemText, Divider, Card } from "@mui/material";
import { Train } from "@src/store/type";
import { useState } from "react";

import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";

function TrainRow(props: {
  train: Train;
  onClick: (clicked: Train) => void;
  onDelete: (id: number, name: string) => void;
}) {
  const [hover, setHover] = useState(false);
  return (
    <ListItem
      secondaryAction={
        hover && (
          <IconButton
            css={css`
              width: 40px;
            `}
            edge="end"
            aria-label="delete"
            onClick={() => {
              props.onDelete(props.train.id, props.train.name);
            }}
          >
            <DeleteIcon />
          </IconButton>
        )
      }
      onMouseOver={() => setHover(true)}
      onMouseOut={() => setHover(false)}
      onDoubleClick={() => props.onClick(props.train)}
      css={css`
        padding: 0px;
      `}
    >
      <ListItemButton
        css={css`
          margin-right: ${hover ? 0 : 32}px;
        `}
      >
        <ListItemText
          css={css`
            width: 200px;
            text-overflow: ellipsis;
          `}
          primary={props.train.name}
        />
        <ListItemText
          css={css`
            width: 220px;
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
    </ListItem>
  );
}

export default function TrainTable(props: {
  trains: Train[];
  onClick: (clicked: Train) => void;
  onDelete: (id: number, name: string) => void;
}) {
  return (
    <Card
      elevation={0}
      css={css`
        height: 600px;
        overflow: auto;
      `}
    >
      <List>
        <ListItem>
          <ListItemText
            css={css`
              width: 200px;
            `}
            primary={"학습명"}
          />
          <ListItemText
            css={css`
              width: 220px;
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
          <ListItemText
            css={css`
              width: 40px;
            `}
            primary={""}
          />
        </ListItem>
        <Divider />
        {props.trains.map((train: Train) => (
          <>
            <TrainRow train={train} onClick={props.onClick} onDelete={props.onDelete} />
            <Divider />
          </>
        ))}
        {props.trains.length === 0 && (
          <div
            css={css`
              height: 500px;
              width: 940px;
              display: flex;
              justify-content: center;
              align-items: center;
            `}
          >
            생성된 학습이 없습니다
          </div>
        )}
      </List>
    </Card>
  );
}
