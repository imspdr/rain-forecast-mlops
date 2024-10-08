import { runInAction, makeAutoObservable } from "mobx";
import { rainAPI } from "./apis";
import { Train, TrainedModel } from "./type";

export class RootStore {
  private _trains: Train[];
  private _trainedModels: TrainedModel[];
  constructor() {
    this._trainedModels = [];
    this._trains = [];
    makeAutoObservable(this);
  }
  get trains() {
    return this._trains;
  }
  get trainedModels() {
    return this._trainedModels;
  }
  set trains(given: Train[]) {
    this._trains = given;
  }
  set trainedModels(given: TrainedModel[]) {
    this._trainedModels = given;
  }

  getTrains = async () => {
    const res = await rainAPI.train.getAll().catch((_) => {
      return [];
    });
    this.trains = res;
  };
  createTrain = async (name: string, startDay: string, endDay: string) => {
    const res = await rainAPI.train.create(name, startDay, endDay);
    this.getTrains();
  };
  deleteTrain = async (id: number) => {
    const res = await rainAPI.train.delete(id);
    this.getTrains();
  };
  getTrainedModels = async () => {
    const res = await rainAPI.model.getAll().catch((_) => {
      return [];
    });
    this._trainedModels = res;
  };
  getTrainedModel = async (name: string) => {
    const res = await rainAPI.model.getTrainedModel(name);
    return res;
  };
  deleteTrainedModel = async (id: number) => {
    const res = await rainAPI.model.delete(id);
    this.getTrainedModels();
  };
  deployTrainedModel = async (id: number) => {
    const res = await rainAPI.model.deploy(id);
    this.getTrainedModels();
  };
  undeployTrainedModel = async (id: number) => {
    const res = await rainAPI.model.undeploy(id);
    this.getTrainedModels();
  };
}
