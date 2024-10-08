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

export type DataDistribution = {
  col_name: string;
  col_type: string;
  distribution: NumericDist | CategoricalDist | [];
};

export type NumericDist = {
  minmax: {
    min: number;
    max: number;
    mean: number;
  };
  histogram: {
    counts: number[];
    bins: number[];
  };
};

export type Base = {
  name: string;
  value: number;
};

export type BaseString = {
  name: string;
  value: string;
};

export type CategoricalDist = {
  value_percentage: Base[];
};

export type TrainedModelInfo = {
  best_config: BaseString[];
  evaluate: Base[];
  feature_importance: {
    label: string[];
    value: number[];
  };
};
