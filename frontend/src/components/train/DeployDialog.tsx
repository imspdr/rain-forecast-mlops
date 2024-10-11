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

export default function DeployDialog(props: {
  open: boolean;
  name: string;
  isDeployed: boolean;
  setOpen: (v: boolean) => void;
  onDeploy: () => void;
}) {
  const handleClose = () => {
    props.setOpen(false);
  };
  const handleComplete = () => {
    props.onDeploy();
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
        <Typography>{`선택한 모델 ${props.name}을 ${
          props.isDeployed ? "배포 취소" : "배포"
        }하시겠습니까?`}</Typography>
      </DialogTitle>
      <DialogContent>
        <Typography variant="caption">{"최대 9개의 모델까지 배포할 수 있습니다."}</Typography>
        <Typography variant="caption">{"모델 배포 후 추론이 가능하기까지 수 분 소요될 수 있습니다.."}</Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disableElevation size="large">
          취소
        </Button>
        <Button
          onClick={handleComplete}
          color="primary"
          variant="contained"
          autoFocus
          disableElevation
          size="large"
        >
          {props.isDeployed ? "배포 취소" : "배포"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
