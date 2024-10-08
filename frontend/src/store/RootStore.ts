import { runInAction, makeAutoObservable } from "mobx";
import { rainAPI } from "./apis";
import { Train, TrainedModel, TrainedModelSimple } from "./type";

type Del = {
  id: number;
  name: string;
  open: boolean;
};
export class RootStore {
  private _trains: Train[];
  private _deployedModels: TrainedModelSimple[];

  private _detail: Train | undefined;
  private _delete: Del;
  constructor() {
    this._trains = [];
    this._deployedModels = [];
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
  get deployedModels() {
    return this._deployedModels;
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
  set deployedModels(given: TrainedModelSimple[]) {
    this._deployedModels = given;
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
  getDeployedTrainedModels = async () => {
    const res = await rainAPI.model.getAllDeployed().catch((_) => {
      return [];
    });
    this._deployedModels = res;
  };
  getTrainedModel = async (name: string) => {
    const res = await rainAPI.model.getTrainedModel(name).catch((_) => undefined);
    return res;
  };

  deployTrainedModel = async (id: number) => {
    await rainAPI.model.deploy(id);
    this.getDeployedTrainedModels();
  };
  undeployTrainedModel = async (id: number) => {
    await rainAPI.model.undeploy(id);
    this.getDeployedTrainedModels();
  };

  infer = async (day: string, name: string) => {
    const res = await rainAPI.kserve.inference(day, name);
    return res;
  };
}
