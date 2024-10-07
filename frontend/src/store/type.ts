export type Train = {
  id: number;
  name: string;
  cpu_size: string;
  memory_size: string;
  start_day: string;
  end_day: string;
  created_at: string;
  finished_at: undefined | string;
  status: string;
};

export type TrainedModel = {
  id: number;
  name: string;
  train_name: string;
  data_distribution: string;
  trained_model_info: string;
  deployed: string;
};
