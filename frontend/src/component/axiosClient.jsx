import axios from "axios";

export const backend1Client = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const backend2Client = axios.create({
  baseURL: 'http://localhost:4000', 
  headers: {
    'Content-Type': 'application/json'
  }
});