import { Route, Routes } from "react-router-dom";
import Auction from "./pages/Auction";
import Home from "./pages/Home";
import MyAuction from "./pages/MyAuction";
import Winnings from "./pages/Winnings";
import Error from "./pages/Error";

const App = () => {
  return (
    <div className="App">
      <Routes>
        <Route path="/Auction" element={<Auction />} />
        <Route path="/MyAuction" element={<MyAuction />} />
        <Route path="/Winnings" element={<Winnings />} />
        <Route exact path="/" element={<Home />} />
        <Route path="*" element={<Error />} />
      </Routes>
    </div>
  );
};

export default App;