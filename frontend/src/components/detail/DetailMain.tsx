import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { TrainedModel } from "@src/store/type";

export default function DetailMain(props: { trainedModel: TrainedModel | undefined }) {
  return <>{props.trainedModel && <div>{props.trainedModel.train_name}</div>}</>;
}
