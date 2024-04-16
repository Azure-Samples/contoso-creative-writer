import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { User } from "./index";

const initialState: User = {
  name: "",
  email: "",
  status: "unauthenticated",
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.name = action.payload.name;
      state.email = action.payload.email;
      state.status = action.payload.status;
    },
  },
});

export const { setUser } = userSlice.actions;
export default userSlice.reducer;
