import Home from './pages/Homepage';
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/game/:gameId" element={<Home />} />
    </Routes>
  );
}

export default App;