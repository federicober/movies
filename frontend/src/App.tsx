import { BrowserRouter, Route, Routes } from "react-router-dom";
import createTheme from "@mui/material/styles/createTheme";
import ThemeProvider from "@mui/material/styles/ThemeProvider";

import Header from "./components/Header";
import Home from "./pages/Home";
import { OpenAPI } from "./client";
import SessionDetails from "./pages/SessionDetails";

const theme = createTheme({
  spacing: 2,
});

OpenAPI.BASE = "http://localhost:8000";

function App() {
  const onLogout = () => {
    console.log("Login out");
  };

  return (
    <ThemeProvider theme={theme}>
      <Header onLogout={onLogout} />
      <BrowserRouter>
        <Routes>
          <Route path="/session/:SessionId" element={<SessionDetails />} />
          <Route path="/" element={<Home />}></Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
