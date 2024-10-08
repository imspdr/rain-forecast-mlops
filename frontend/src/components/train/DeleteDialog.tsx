import { css } from "@emotion/react";
import { Button, Dialog, DialogTitle, DialogContent, DialogActions } from "@mui/material";

export default function DeleteDialog(props: {
  open: boolean;
  setOpen: (v: boolean) => void;
  name: string;
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
          width: 800px;
        }
      `}
      maxWidth={false}
    >
      <DialogContent>{`학습 ${props.name}을 삭제하시겠습니까?`}</DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>취소</Button>
        <Button onClick={handleComplete} color="primary" autoFocus>
          삭제
        </Button>
      </DialogActions>
    </Dialog>
  );
}
