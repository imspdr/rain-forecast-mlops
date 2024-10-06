import axios from "axios";
import crawlSample from "./crawlSample.json";
import { MovieData } from "./type";

const namespace = "default"
const modelname = ""

const rainURL = `/api/v1/models/${modelname}:predict`;
const rainHost = `rain-multi-model.${namespace}.example.com`;


export const rainAPI={};
