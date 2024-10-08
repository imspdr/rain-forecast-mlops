import axios from "axios";
import { Train, TrainedModel } from "./type";

const namespace = "default";
const modelname = "";
const backend = "/api";

const rainURL = `/api/v1/models/${modelname}:predict`;
const rainHost = `rain-multi-model.${namespace}.example.com`;

export const rainAPI = {
  train: {
    create: async (name: string, startDay: string, endDay: string) => {
      const url = `${backend}/train/`;
      const res = await axios.post<void>(
        url,
        {
          name: name,
          start_day: startDay,
          end_day: endDay,
          cpu_size: "1000m",
          memory_size: "1Gi",
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      if (axios.isAxiosError(res)) throw res;
      return res.data;
    },
    getAll: async () => {
      const url = `${backend}/train/all/`;
      const res = await axios.get<Train[]>(url);
      if (axios.isAxiosError(res)) throw res;
      return res.data as Train[];
    },
    delete: async (id: number) => {
      const url = `${backend}/train/${id}`;
      const res = await axios.delete<void>(url);
      if (axios.isAxiosError(res)) throw res;
      return res.data;
    },
  },
  model: {
    getAll: async () => {
      const url = `${backend}/trained_model/all/`;
      const res = await axios.get<TrainedModel[]>(url);
      if (axios.isAxiosError(res)) throw res;
      return res.data;
    },
    getTrainedModel: async (name: string) => {
      const url = `${backend}/trained_model/${name}`;
      const res = await axios.get<TrainedModel>(url);
      if (axios.isAxiosError(res)) throw res;
      return res.data;
    },
    delete: async (id: number) => {
      const url = `${backend}/trained_model/${id}`;
      const res = await axios.delete<void>(url);
      if (axios.isAxiosError(res)) throw res;
      return res.data;
    },
    deploy: async (id: number) => {
      const url = `${backend}/trained_model/deploy/${id}`;
      const res = await axios.put<void>(url);
      if (axios.isAxiosError(res)) throw res;
      return res.data;
    },
    undeploy: async (id: number) => {
      const url = `${backend}/trained_model/undeploy/${id}`;
      const res = await axios.put<void>(url);
      if (axios.isAxiosError(res)) throw res;
      return res.data;
    },
  },
};
