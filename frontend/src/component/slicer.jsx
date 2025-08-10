import { createSlice } from "@reduxjs/toolkit";

const reactSlice = createSlice({
  name: "slice1",
  initialState: { userId: null },
  reducers: {
    setUserId : (state,actions) => {state.userId = actions.payload}
  },
});

export default reactSlice.reducer;
export const {setUserId} = reactSlice.actions;