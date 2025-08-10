import { configureStore } from "@reduxjs/toolkit";
import reactReducer from "./slicer";

const store = configureStore({
  reducer: {
    slice1: reactReducer,
  },
});

export default store;