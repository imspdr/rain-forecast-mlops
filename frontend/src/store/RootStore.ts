import { runInAction, makeAutoObservable } from "mobx";
import { rainAPI } from "./apis";
import { Train, TrainedModel } from "./type";

type Del = {
  id: number;
  name: string;
  open: boolean;
};
export class RootStore {
  private _trains: Train[];
  private _trainedModels: TrainedModel[];
  private _detail: Train | undefined;
  private _delete: Del;
  constructor() {
    this._trainedModels = [];
    this._trains = [];
    this._detail = undefined;
    this._delete = {
      id: -1,
      name: "",
      open: false,
    };
    makeAutoObservable(this);
  }
  get trains() {
    return this._trains;
  }
  get trainedModels() {
    return this._trainedModels;
  }
  get detail() {
    return this._detail;
  }
  get delete() {
    return this._delete;
  }
  set trains(given: Train[]) {
    this._trains = given;
  }
  set trainedModels(given: TrainedModel[]) {
    this._trainedModels = given;
  }
  set detail(given: Train | undefined) {
    this._detail = given;
  }
  set delete(given: Del) {
    this._delete = given;
  }

  getTrains = async () => {
    const res = await rainAPI.train.getAll().catch((_) => {
      return [];
    });
    this.trains = res;
  };
  createTrain = async (name: string, startDay: string, endDay: string) => {
    await rainAPI.train.create(name, startDay, endDay);
    this.getTrains();
  };
  deleteTrain = async () => {
    await rainAPI.train.delete(this.delete.id);
    await rainAPI.model.delete(this.delete.name);

    this.getTrains();
  };
  getTrainedModels = async () => {
    const res = await rainAPI.model.getAll().catch((_) => {
      return [];
    });
    this._trainedModels = res;
  };
  getTrainedModel = async (name: string) => {
    const res = await rainAPI.model.getTrainedModel(name).catch((_) => undefined);
    return res;
  };

  deployTrainedModel = async (id: number) => {
    await rainAPI.model.deploy(id);
    this.getTrainedModels();
  };
  undeployTrainedModel = async (id: number) => {
    await rainAPI.model.undeploy(id);
    this.getTrainedModels();
  };
}
