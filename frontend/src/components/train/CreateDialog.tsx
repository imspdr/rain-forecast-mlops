import { observer } from "mobx-react";
import { css } from "@emotion/react";
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import { properDate } from "@src/store/util";

const alphanumericPattern = /^[a-zA-Z0-9]*$/;

export function DateText(props: { label: string; day: string; setDay: (v: string) => void }) {
  const [validation, setValidation] = useState(true);
  useEffect(() => {
    setValidation(properDate(props.day));
  }, [props.day]);
  return (
    <TextField
      error={!validation}
      label={`${props.label} (YYYYMMDD)`}
      helperText={validation ? "" : "날짜 포맷을 지켜주세요 (2020년 이후)"}
      variant="outlined"
      value={props.day}
      css={css`
        width: 250px;
      `}
      onChange={(e) => {
        props.setDay(e.target.value);
      }}
    />
  );
}

function generateDateName() {
  const now = new Date();

  const year = String(now.getFullYear());
  const month = String(now.getMonth() + 1).padStart(2, "0"); // Ensure 2 digits
  const day = String(now.getDate()).padStart(2, "0"); // Ensure 2 digits
  const hours = String(now.getHours()).padStart(2, "0"); // Ensure 2 digits
  const minutes = String(now.getMinutes()).padStart(2, "0"); // Ensure 2 digits
  const seconds = String(now.getSeconds()).padStart(2, "0"); // Ensure 2 digits

  const formattedDateTime = `${year.slice(2)}${month}${day}${hours}${minutes}${seconds}`;
  return formattedDateTime;
}
export default function CreateDialog(props: {
  open: boolean;
  setOpen: (v: boolean) => void;
  onCreate: (name: string, startDay: string, endDay: string) => void;
}) {
  const [name, setName] = useState(`train${generateDateName()}`);
  const [startDay, setStartDay] = useState("20230427");
  const [endDay, setEndDay] = useState("20240427");
  const [validation, setValidation] = useState(true);
  useEffect(() => {
    setValidation(alphanumericPattern.test(name) && name.length > 3 && name.length < 18);
  }, [name]);

  const handleClose = () => {
    props.setOpen(false);
  };
  const handleComplete = () => {
    if (properDate(startDay) && properDate(endDay) && alphanumericPattern.test(name) && name) {
      props.onCreate(name, startDay, endDay);
      props.setOpen(false);
    } else {
      setValidation(alphanumericPattern.test(name) && name.length > 3);
    }
  };
  return (
    <Dialog
      open={props.open}
      onClose={handleClose}
      css={css`
        & .MuiDialog-paper {
          width: 600px;
          padding: 10px;
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
            gap: 20px;
          `}
        >
          <Typography>데이터 수집 범위</Typography>
          <div
            css={css`
              display: flex;
              flex-direction: row;
              align-items: flex-start;
              justify-content: space-between;
              height: 100px;
            `}
          >
            <DateText label={"시작 날짜"} day={startDay} setDay={setStartDay} />
            <Typography>~</Typography>
            <DateText label={"마지막 날짜"} day={endDay} setDay={setEndDay} />
          </div>
          <Typography>학습명</Typography>
          <div
            css={css`
              height: 80px;
              width: 560px;
            `}
          >
            <TextField
              error={!validation}
              variant="outlined"
              value={name}
              onChange={(e) => {
                setName(e.target.value);
              }}
              helperText={
                validation
                  ? ""
                  : "학습 명에는 4자 이상, 18자 미만의 알파벳과 숫자 조합만 사용가능합니다"
              }
            />
          </div>
        </div>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disableElevation size="large">
          취소
        </Button>
        <Button
          onClick={handleComplete}
          variant="contained"
          autoFocus
          disableElevation
          size="large"
        >
          생성
        </Button>
      </DialogActions>
    </Dialog>
  );
}
