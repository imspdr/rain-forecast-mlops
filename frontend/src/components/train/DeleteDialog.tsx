import { css } from "@emotion/react";
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
} from "@mui/material";
import { useState } from "react";

export default function DeleteDialog(props: {
  open: boolean;
  name: string;
  setOpen: (v: boolean) => void;
  onDelete: () => void;
}) {
  const handleClose = () => {
    props.setOpen(false);
  };
  const handleComplete = () => {
    props.onDelete();
    props.setOpen(false);
  };
  return (
    <Dialog
      open={props.open}
      onClose={handleClose}
      css={css`
        & .MuiDialog-paper {
          width: 500px;
          padding: 10px;
        }
      `}
      maxWidth={false}
    >
      <DialogTitle>
        <Typography>{`선택한 학습 ${props.name}을 삭제하시겠습니까?`}</Typography>
      </DialogTitle>
      <DialogActions>
        <Button onClick={handleClose} disableElevation size="large">
          취소
        </Button>
        <Button
          onClick={handleComplete}
          color="error"
          variant="contained"
          autoFocus
          disableElevation
          size="large"
        >
          삭제
        </Button>
      </DialogActions>
    </Dialog>
  );
}
