import { observer } from "mobx-react";
import { css } from "@emotion/react";
import { Button, Dialog, DialogTitle, DialogContent, DialogActions } from "@mui/material";
import ClearIcon from "@mui/icons-material/Clear";
import { useState } from "react";

export default function CreateDialog(props: {
  open: boolean;
  setOpen: (v: boolean) => void;
  onCreate: (name: string, startDay: string, endDay: string) => void;
}) {
  const [name, setName] = useState("");
  const [startDay, setStartDay] = useState("");
  const [endDay, setEndDay] = useState("");

  const handleClose = () => {
    props.setOpen(false);
  };
  const handleComplete = () => {
    props.onCreate(name, startDay, endDay);
    props.setOpen(false);
  };
  return (
    <Dialog
      open={props.open}
      onClose={handleClose}
      css={css`
        & .MuiDialog-paper {
          height: 600px;
          width: 800px;
        }
      `}
      maxWidth={false}
    >
      <DialogTitle>{"새 학습 생성하기"}</DialogTitle>
      <DialogContent>
        <div
          css={css`
            padding: 10px;
            display: flex;
            flex-direction: column;
            gap: 30px;
          `}
        ></div>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>취소</Button>
        <Button onClick={handleComplete} color="primary" autoFocus>
          생성
        </Button>
      </DialogActions>
    </Dialog>
  );
}
