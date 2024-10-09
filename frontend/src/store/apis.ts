import axios from "axios";
import { Train, TrainedModel, TrainedModelSimple } from "./type";

const namespace = "TOENVNAMESPACE";
const backend = "/api";

const rainHost = `rain-multi-model.${namespace}.example.com`;

export const rainAPI = {
  kserve: {
    inference: async (day: string, modelname: string) => {
      const rainURL = `/kserve/v1/models/${modelname}:predict`;
      const ret = await axios
        .post(
          rainURL,
          {
            instances: [day],
          },
          {
            headers: {
              "Content-Type": "application/json",
              "Kserve-Host": rainHost,
            },
          }
        )
        .then((data: any) => {
          return data.data;
        })
        .catch((e) => {
          return {
            predictions: [
              {
                y_hat: [],
                y_true: [],
                y_proba: [],
              },
            ],
          };
        });
      // const ret = {
      //   predictions: [
      //     {
      //       y_hat: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      //       y_true: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1],
      //       y_proba: [
      //         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0001, 0.0031,
      //         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      //       ],
      //     },
      //   ],
      // };
      return ret;
    },
  },
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
    getAllDeployed: async () => {
      const url = `${backend}/trained_model/all/deployed`;
      const res = await axios.get<TrainedModelSimple[]>(url);
      if (axios.isAxiosError(res)) throw res;
      return res.data;
    },
    getTrainedModel: async (name: string) => {
      const url = `${backend}/trained_model/${name}`;
      const res = await axios.get<TrainedModel>(url);
      if (axios.isAxiosError(res)) throw res;
      return res.data;
    },
    delete: async (name: string) => {
      const url = `${backend}/trained_model/name/${name}`;
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
