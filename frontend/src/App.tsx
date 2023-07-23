import { BrowserRouter, Route, Routes } from "react-router-dom";
import createTheme from "@mui/material/styles/createTheme";
import ThemeProvider from "@mui/material/styles/ThemeProvider";

import Header from "./components/Header";
import Root from "./pages/Root";

function App() {
  const theme = createTheme({
    spacing: 2,
  });

  const onLogout = () => {
    console.log("Login out");
  };

  return (
    <ThemeProvider theme={theme}>
      <Header onLogout={onLogout} />
      <BrowserRouter>
        <Routes>
          {/* <Route
            path="/session/:SessionId"
            element={<Session />}
          /> */}
          <Route path="/*" element={<Root />}></Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
