import { css } from "@emotion/react";
import WbSunnyOutlinedIcon from "@mui/icons-material/WbSunnyOutlined";
import WaterDropOutlinedIcon from "@mui/icons-material/WaterDropOutlined";
import QuestionMarkIcon from "@mui/icons-material/QuestionMark";
import { Divider } from "@mui/material";

const isOk = (y: number | undefined) => {
  return y == 0 || !!y;
};

//y_pred, y_proba, y_hat
function ResultIcon(props: { y: number }) {
  return (
    <>
      {props.y === 1 ? (
        <WaterDropOutlinedIcon />
      ) : props.y === 0 ? (
        <WbSunnyOutlinedIcon />
      ) : (
        <QuestionMarkIcon />
      )}
    </>
  );
}

function ResultSingle(props: {
  time: number;
  yHat: number | undefined;
  yTrue: number | undefined;
  yProba: number | undefined;
}) {
  const { time, yHat, yTrue, yProba } = props;
  return (
    <>
      {isOk(yHat) && isOk(yTrue) && isOk(yProba) && (
        <div
          css={css`
            display: flex;
            flex-direction: row;
            height: 35px;
            align-items: center;
          `}
        >
          <div
            css={css`
              width: 50px;
            `}
          >
            {`${time}시`}
          </div>
          <div
            css={css`
              width: 200px;
              display: flex;
              flex-direction: row;
              justify-content: space-between;
              align-items: center;
            `}
          >
            <div>
              <ResultIcon y={yHat!} />
              <span
                css={css`
                  margin-left: 5px;
                  font-size: 12px;
                `}
              >{`강수 확률: ${(yProba! * 100).toFixed(2)}%`}</span>
            </div>
            <ResultIcon y={yTrue!} />
          </div>
        </div>
      )}
    </>
  );
}

export default function InferResult(props: { yHat: number[]; yTrue: number[]; yProba: number[] }) {
  const timeArray = [];
  for (let i = 1; i < 25; i++) {
    timeArray.push(i);
  }
  return (
    <div
      css={css`
        display: flex;
        flex-direction: row;
        height: 450px;
        gap: 30px;
      `}
    >
      <div
        css={css`
          display: flex;
          flex-direction: column;
        `}
      >
        <div
          css={css`
            display: flex;
            flex-direction: row;

            margin-left: 50px;
            margin-bottom: 10px;
            width: 200px;
            justify-content: space-between;
          `}
        >
          <span>추론</span>
          <span>실제</span>
        </div>
        {timeArray
          .filter((i) => i < 13)
          .map((i) => {
            return (
              <ResultSingle
                time={i}
                yHat={props.yHat[i - 1]}
                yTrue={props.yTrue[i - 1]}
                yProba={props.yProba[i - 1]}
              />
            );
          })}
      </div>
      <Divider orientation="vertical" />
      <div
        css={css`
          display: flex;
          flex-direction: column;
        `}
      >
        <div
          css={css`
            display: flex;
            flex-direction: row;
            width: 200px;
            margin-left: 50px;
            margin-bottom: 10px;
            justify-content: space-between;
          `}
        >
          <span>추론</span>
          <span>실제</span>
        </div>
        {timeArray
          .filter((i) => i >= 13)
          .map((i) => {
            return (
              <ResultSingle
                time={i}
                yHat={props.yHat[i - 1]}
                yTrue={props.yTrue[i - 1]}
                yProba={props.yProba[i - 1]}
              />
            );
          })}
      </div>
    </div>
  );
}
