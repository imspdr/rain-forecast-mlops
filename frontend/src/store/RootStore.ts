import { runInAction, makeAutoObservable } from "mobx";
import { rainAPI } from "./apis";

export class RootStore {

  constructor() {
    makeAutoObservable(this);
  }
}
